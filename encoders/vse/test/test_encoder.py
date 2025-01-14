"""
Tests for module encoder

@author: Damares Resende
@contact: damaresresende@usp.br
@since: June 16, 2020

@organization: University of Sao Paulo (USP)
    Institute of Mathematics and Computer Science (ICMC)
    Laboratory of Visualization, Imaging and Computer Graphics (VICG)
"""
import unittest
import numpy as np
from scipy.io import loadmat

from encoders.vse.src.encoder import ModelFactory, ModelType, Encoder


class EncoderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Builds and train AE model
        """
        data = loadmat('../../../../Datasets/SEM/cub_demo_data.mat')
        input_length = output_length = data['X_tr'].shape[1] + data['S_tr'].shape[1]
        cls.ae = Encoder(input_length, data['S_tr'].shape[1], output_length, ModelType.SIMPLE_AE, 5)

        labels = data['te_cl_id']
        labels_dict = {labels[i][0]: attributes for i, attributes in enumerate(data['S_te_pro'])}
        s_te = np.array([labels_dict[label[0]] for label in data['test_labels_cub']])
        cls.ae.estimate_semantic_data(data['X_tr'], data['X_te'], data['S_tr'], s_te)

    def test_simple_ae(self):
        """
        Tests if auto encoder model is build with the correct size fo input, output and encoding
        """
        model = ModelFactory(2048, 128, 2048)(ModelType.SIMPLE_AE)

        self.assertEqual([(None, 2048)], model.layers[0].input_shape)
        self.assertEqual((None, 128), model.layers[5].output_shape)
        self.assertEqual((None, 2048), model.layers[-1].output_shape)

    def test_factory_call_ae(self):
        """
        Tests if the correct type of AE is returned in call method
        """
        model = ModelFactory(2048, 128, 2048)(ModelType.SIMPLE_AE)

        self.assertEqual([(None, 2048)], model.get_layer('ae_input').input_shape)
        self.assertEqual((None, 128), model.get_layer('code').output_shape)
        self.assertEqual((None, 2048), model.get_layer('ae_output').output_shape)

    def test_estimate_semantic_data_awa_ae(self):
        """
        Tests if result from semantic data estimation is in the correct shape for awa
        """
        data = loadmat('../../../../Datasets/SEM/awa_demo_data.mat')
        input_length = output_length = data['X_tr'].shape[1] + data['S_tr'].shape[1]
        ae = Encoder(input_length, data['S_tr'].shape[1], output_length, ModelType.SIMPLE_AE_1L, 1)

        labels = data['param']['testclasses_id'][0][0]
        labels_dict = {labels[i][0]: attributes for i, attributes in enumerate(data['S_te_pro'])}
        s_te = np.array([labels_dict[label[0]] for label in data['param']['test_labels'][0][0]])

        sem_tr, sem_te = ae.estimate_semantic_data(data['X_tr'], data['X_te'], data['S_tr'], s_te)

        self.assertEqual((data['X_tr'].shape[0], data['S_tr'].shape[1]), sem_tr.shape)
        self.assertEqual((data['X_te'].shape[0], data['S_tr'].shape[1]), sem_te.shape)

    def test_estimate_semantic_data_cub_ae(self):
        """
        Tests if result from semantic data estimation is in the correct shape for cub
        """
        data = loadmat('../../../../Datasets/SEM/cub_demo_data.mat')
        input_length = output_length = data['X_tr'].shape[1] + data['S_tr'].shape[1]
        ae = Encoder(input_length, data['S_tr'].shape[1], output_length, ModelType.SIMPLE_AE_1L, 1)

        labels = data['te_cl_id']
        labels_dict = {labels[i][0]: attributes for i, attributes in enumerate(data['S_te_pro'])}
        s_te = np.array([labels_dict[label[0]] for label in data['test_labels_cub']])

        sem_tr, sem_te = ae.estimate_semantic_data(data['X_tr'], data['X_te'], data['S_tr'], s_te)

        self.assertEqual((data['X_tr'].shape[0], data['S_tr'].shape[1]), sem_tr.shape)
        self.assertEqual((data['X_te'].shape[0], data['S_tr'].shape[1]), sem_te.shape)
