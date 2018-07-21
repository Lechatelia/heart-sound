import tensorflow as tf
import  numpy as np

INPUT_NODE = 577
OUTPUT_NODE = 5
LAYER1_NODE = 300
NODE1=70
NODE2=30
NODE3=80
NODE4=20
NODE5=20
NODE6=80
LAYER2_NODE = 100
LAYER3_NODE = 100

def get_weight_variable(shape, regularizer):
    weights = tf.get_variable("weights", shape, initializer=tf.truncated_normal_initializer(stddev=0.1))
    if regularizer != None: tf.add_to_collection('losses', regularizer(weights))
    return weights

def my_get_weight_variable(name,shape, regularizer):
    weights = tf.get_variable(name, shape, initializer=tf.truncated_normal_initializer(stddev=0.1))
    if regularizer != None: tf.add_to_collection('losses', regularizer(weights))
    return weights

def inference(input_tensor, regularizer,keep_prob=1):
    with tf.variable_scope('layer1'):

        #weights1_1 = tf.get_variable("weights1", [40,10], initializer=tf.truncated_normal_initializer(stddev=0.1))
        weights1_1=my_get_weight_variable("weights1", [40,NODE1],regularizer)
        biases1_1 = tf.get_variable("biases1", [NODE1], initializer=tf.constant_initializer(1.0))
        layer1_1 = tf.nn.relu(tf.matmul(input_tensor[: ,0:40], weights1_1) + biases1_1)
        layer1_1=tf.nn.dropout(layer1_1,keep_prob)

        #weights1_2 = tf.get_variable("weights2", [12,5], initializer=tf.truncated_normal_initializer(stddev=0.1))
        weights1_2 = my_get_weight_variable("weights2", [12, NODE2], regularizer)
        biases1_2 = tf.get_variable("biases2", [NODE2], initializer=tf.constant_initializer(1.0))
        layer1_2 = tf.nn.relu(tf.matmul(input_tensor[:,40:52], weights1_2) + biases1_2)
        layer1_2 = tf.nn.dropout(layer1_2, keep_prob)

        #weights1_3 = tf.get_variable("weights3", [128,20], initializer=tf.truncated_normal_initializer(stddev=0.1))
        weights1_3 = my_get_weight_variable("weights3", [128, NODE3], regularizer)
        biases1_3 = tf.get_variable("biases3", [NODE3], initializer=tf.constant_initializer(1.0))
        layer1_3 = tf.nn.relu(tf.matmul(input_tensor[:,52:180], weights1_3) + biases1_3)
        layer1_3 = tf.nn.dropout(layer1_3, keep_prob)

        #weights1_4 =  tf.get_variable("weights4", [7,5], initializer=tf.truncated_normal_initializer(stddev=0.1))
        weights1_4 = my_get_weight_variable("weights4", [7, NODE4], regularizer)
        biases1_4 = tf.get_variable("biases4", [NODE4], initializer=tf.constant_initializer(0.0))
        layer1_4 = tf.nn.relu(tf.matmul(input_tensor[:,180:187], weights1_4) + biases1_4)
        layer1_4 = tf.nn.dropout(layer1_4, keep_prob)

        #weights1_5 = tf.get_variable("weights5", [6,5], initializer=tf.truncated_normal_initializer(stddev=0.1))
        weights1_5 = my_get_weight_variable("weights5", [6, NODE5], regularizer)
        biases1_5 = tf.get_variable("biases5", [NODE5], initializer=tf.constant_initializer(0.0))
        layer1_5 = tf.nn.relu(tf.matmul(input_tensor[:,187:193], weights1_5) + biases1_5)
        layer1_5 = tf.nn.dropout(layer1_5, keep_prob)

        #weights1_6 =tf.get_variable("weights6", [384,40], initializer=tf.truncated_normal_initializer(stddev=0.1))
        weights1_6 = my_get_weight_variable("weights6", [384,NODE6], regularizer)
        biases1_6 = tf.get_variable("biases6", [NODE6], initializer=tf.constant_initializer(0.0))
        layer1_6 = tf.nn.relu(tf.matmul(input_tensor[:,193: ], weights1_6) + biases1_6)
        layer1_6 = tf.nn.dropout(layer1_6, keep_prob)

        layer1 = tf.concat([layer1_1,layer1_2,layer1_3,layer1_4,layer1_5,layer1_6],1)

    # with tf.variable_scope('layer2'):
    #     weights = get_weight_variable([LAYER1_NODE, OUTPUT_NODE], regularizer)
    #     biases = tf.get_variable("biases", [OUTPUT_NODE], initializer=tf.constant_initializer(1.0))
    #     layer2 = tf.matmul(layer1, weights) + biases
    #     layer2 = tf.nn.dropout(layer2, keep_prob)

    with tf.variable_scope('layer2'):
        weights = get_weight_variable([LAYER1_NODE, LAYER2_NODE], regularizer)
        biases = tf.get_variable("biases", [LAYER2_NODE], initializer=tf.constant_initializer(0.0))
        layer2 = tf.nn.relu(tf.matmul(layer1, weights) + biases)
        layer2 = tf.nn.dropout(layer2, keep_prob)

    with tf.variable_scope('layer_res'):
        weights = tf.get_variable("weights_res", [LAYER2_NODE,LAYER2_NODE],initializer=tf.truncated_normal_initializer(stddev=0.1))
        # weights = get_weight_variable([LAYER2_NODE, LAYER2_NODE], regularizer)
        biases = tf.get_variable("biases", [LAYER2_NODE], initializer=tf.constant_initializer(0.0))
        layer3_1 = tf.nn.relu(tf.matmul(layer2, weights) + biases)

        weights = tf.get_variable("weights_res_1", [LAYER2_NODE, LAYER2_NODE],
                                  initializer=tf.truncated_normal_initializer(stddev=0.1))
        # weights = get_weight_variable([LAYER2_NODE, LAYER2_NODE], regularizer)
        biases = tf.get_variable("biases_1", [LAYER2_NODE], initializer=tf.constant_initializer(0.0))
        layer3_1 = tf.nn.relu(tf.matmul(layer3_1, weights) + biases)
        # layer3_1 = tf.nn.dropout(layer3_1, keep_prob)
        layer3_1+=layer2



    with tf.variable_scope('layer3'):

        weights = get_weight_variable([LAYER2_NODE, OUTPUT_NODE], regularizer)
        biases = tf.get_variable("biases", [OUTPUT_NODE], initializer=tf.constant_initializer(0.0))
        layer3 = tf.nn.relu(tf.matmul(layer3_1, weights) + biases)
        # layer3 = tf.nn.dropout(layer3, keep_prob)

    # with tf.variable_scope('layer4'):
    #     weights = get_weight_variable([LAYER3_NODE, OUTPUT_NODE], regularizer)
    #     biases = tf.get_variable("biases", [OUTPUT_NODE], initializer=tf.constant_initializer(1.0))
    #     layer4 = tf.matmul(layer3, weights) + biases
    #     layer4 = tf.nn.dropout(layer4, keep_prob)

    return layer3