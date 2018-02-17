mkdir ../cache
mkdir ../corpus
mkdir ../models

# context2vector pre-trained models
wget http://irsrv2.cs.biu.ac.il/downloads/context2vec/context2vec.mscc.model.package.tar.gz -P ../cache
wget http://irsrv2.cs.biu.ac.il/downloads/context2vec/context2vec.ukwac.model.package.tar.gz -P ../cache

# GloVe word vectors pre-trained on Twitter corpus
wget http://nlp.stanford.edu/data/glove.twitter.27B.zip -P ../cache

# Bataclan twitte corpus
wget https://github.com/edupoux/MVA_2018_SL/blob/master/TD_%233/CorpusBataclan_en.1M.raw.txt.gz -P ../cache

# Decompress data files
tar -xzvf cache/context2vec.mscc.model.package.tar.gz -C ../models/c2v.mscc.model
tar -xzvf cache/context2vec.ukwac.model.package.tar.gz -C ../models/c2v.ukwac.model
tar -xzvf cache/CorpusBataclan_en.1M.raw.txt.gz -C ../corpus
