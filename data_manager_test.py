# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import unittest
from data_manager import DataManager


class DataManagerTest(unittest.TestCase):
  def test_get_masked_image(self):
    image = np.ones((80, 80, 3))
    
    data_manager = DataManager()
    masked_image = data_manager._get_masked_image(image)

    # Shape check
    self.assertTrue( masked_image.shape == (80,80,3) )

    # Every element of masked image should be equal or smaller than original's
    self.assertTrue( (masked_image <= image).all() )
    

  def test_next_masked_batch(self):
    data_manager = DataManager()
    data_manager.prepare()
    
    masked_xs, xs = data_manager.next_masked_batch(100)

    self.assertTrue( len(xs) == 100 )
    self.assertTrue( len(masked_xs) == 100 )

    for i in range(100):
      # Shape check
      self.assertTrue( xs[i].shape == (80,80,3) )
      self.assertTrue( masked_xs[i].shape == (80,80,3) )
      # Every element of masked image should be equal or smaller than original's
      self.assertTrue( (masked_xs[i] <= xs[i]).all() )

      # Elements in image is 0.0 ~ 1.0
      self.assertTrue( np.amax(xs[i]) <= 1.0 )
      self.assertTrue( np.amin(xs[i]) >= 0.0 )
      self.assertTrue( np.amax(masked_xs[i]) <= 1.0 )
      self.assertTrue( np.amin(masked_xs[i]) >= 0.0 )

      self.assertTrue( xs[i].dtype == np.float32 )      
      self.assertTrue( masked_xs[i].dtype == np.float32 )


  def test_next_batch(self):
    data_manager = DataManager()
    data_manager.prepare()

    xs, labels = data_manager.next_batch(100, use_labels=True)
    
    self.assertTrue( len(xs) == 100 )
    self.assertTrue( len(labels) == 100 )

    for i in range(100):
      # Shape check
      self.assertTrue( xs[i].shape == (80,80,3) )
      self.assertTrue( labels[i].shape == (51,) )
      
      # Elements in image is 0.0 ~ 1.0
      self.assertTrue( np.amax(xs[i]) <= 1.0 )
      self.assertTrue( np.amin(xs[i]) >= 0.0 )
      self.assertTrue( xs[i].dtype == np.float32 )

      self.assertTrue( np.amax(labels[i]) <= 1.0 )
      self.assertTrue( np.amin(labels[i]) >= 0.0 )
      self.assertTrue( labels[i].dtype == np.float32 )      
    
  
  def test_index_to_labels(self):
    data_manager = DataManager()
    labels = data_manager._index_to_labels(0)

    # Shape check
    self.assertTrue( labels.shape == (51,) )

    for i in range(51):
      if i == 0 or i == 16 or i == 32 or i == 48:
        labels[i] == 1.0
      else:
        labels[i] == 0.0
    

if __name__ == '__main__':
  unittest.main()
