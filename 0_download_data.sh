mkdir data

# context2vector pre-trained models
wget http://irsrv2.cs.biu.ac.il/downloads/context2vec/context2vec.mscc.model.package.tar.gz -P ./data/
wget http://irsrv2.cs.biu.ac.il/downloads/context2vec/context2vec.ukwac.model.package.tar.gz -P ./data/

# GloVe word vectors pre-trained on Twitter corpus
wget http://nlp.stanford.edu/data/glove.twitter.27B.zip -P ./data/

# Bataclan twitte corpus
wget https://github.com/edupoux/MVA_2018_SL/blob/master/TD_%233/CorpusBataclan_en.1M.raw.txt.gz -P ./data/

# Decompress data files
tar -xzvf data/context2vec.mscc.model.package.tar.gz -C ./data/c2v.mscc.model
tar -xzvf data/context2vec.ukwac.model.package.tar.gz -C ./data/c2v.ukwac.model
tar -xzvf data/CorpusBataclan_en.1M.raw.txt.gz -C ./data
