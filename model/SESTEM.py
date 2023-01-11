import numpy.linalg
import numpy as np
import pandas as pd
import pickle
import sys 

class SESTEM:
  '''
  # Example usage.

  model = SESTEM(article_set=article_set, 
                 labels=labels)
  model.calculate_W_hat()
  model.calculate_D_hat()
  model.train_O()
  predicted_p = model.predict(article_word_rate=new_article, 
                              p_initial=0.5,
                              iterate=1000,
                              lambda_=0.01
                              alpha=0.0001)
  '''
  import numpy as np

  def __init__(self, article_set=[], labels=[], O_plus_hat=[], O_minus_hat=[]):
    self.article_set = article_set
    self.labels = labels
    self.num_articles = len(labels)
    self.O_plus_hat = O_plus_hat
    self.O_minus_hat = O_minus_hat
    assert len(article_set) == self.num_articles, "len(article_set) != len(labels)"
  
  def calculate_W_hat(self):
    # Calculating p_hats list
    s = sorted(self.labels)
    self.p_hats = []

    for label in self.labels:
      i = s.index(label)
      self.p_hats.append(i / self.num_articles)

    # Calculating W_hats list
    self.W_hats = [[p, 1 - p] for p in self.p_hats]
    self.W_hats = np.array(self.W_hats).T
    return self.W_hats
  
  def calculate_D_hat(self):
    self.D_hats = []

    for article in self.article_set:
      rate_sum = 0
      for rate in article:
        rate_sum += rate
      if rate_sum == 0:
        self.D_hats.append(np.array(article))
      else:
        self.D_hats.append(np.array(article) / rate_sum)

    self.D_hats = np.array(self.D_hats).T
    return self.D_hats

  def train_O(self):
    assert (self.D_hats is not None) and (self.W_hats is not None), "D_hats and W_hats are not defined."

    W_T = self.W_hats.T
    temp1 = np.matmul(self.D_hats, W_T)
    temp2 = np.linalg.inv(np.matmul(self.W_hats, W_T))
    X = np.matmul(temp1, temp2)
    X_T = X.T

    self.O_plus_hat = X_T[0]
    self.O_minus_hat = X_T[1]
    return X_T

  def predict(self, article_word_rate, p_initial, iterate, lambda_, alpha):
    p = p_initial
    total_word_sum = 0
    length = len(article_word_rate)
    assert length == len(self.O_plus_hat), "len(article_word_rate) != len(self.O_plus_hat)"
    for rate in article_word_rate:
      total_word_sum += rate
    if total_word_sum == 0: return np.nan
    # Using simple gradient ascend
    for i in range(iterate):
      decay = lambda_ * (1 - 2 * p) / ((1 - p) * p)
      sum_ = 0
      for i in range(length):
        sum_ += (
                  article_word_rate[i] * (self.O_plus_hat[i] - self.O_minus_hat[i]) 
                  / (p * self.O_plus_hat[i] + (1 - p) * self.O_minus_hat[i])
                )

      der_categorical_crossentropy = sum_ / total_word_sum + decay
      p += alpha * der_categorical_crossentropy
    
    return p


if __name__ == '__main__':
    rateFilePath = './data/articleRate.pickle'
    with open(rateFilePath, 'rb') as R:
        rateList = pickle.load(R)
    R.close()
    samsung_file_path = './data/samsung_articles_with_stock(final).dat'
    articleDF = pd.read_pickle(samsung_file_path)
    article_related_stock = articleDF['after_stock'] - articleDF['before_stock']
    print(len(rateList))
    print(len(article_related_stock))
    
    nn = np.isnan(article_related_stock)
    index = 0
    for n in nn:
        if n:
            article_related_stock[index] = 0
        index += 1

    model = SESTEM(rateList, article_related_stock)
    model.calculate_W_hat()
    model.calculate_D_hat()
    O = model.train_O()
    print(O)

    toOfilePath = sys.argv[1] #'/home/aicp05/data/O.pickle'
    print("Output:", toOfilePath)
    with open(toOfilePath, 'wb') as OF:
        pickle.dump(O, OF)
    OF.close()
    
