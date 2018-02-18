mkdir -p ./cache

# clone context2vec repo.
git clone https://github.com/orenmel/context2vec.git

# context2vector pre-trained models
wget http://irsrv2.cs.biu.ac.il/downloads/context2vec/context2vec.mscc.model.package.tar.gz -P ./cache
wget http://irsrv2.cs.biu.ac.il/downloads/context2vec/context2vec.ukwac.model.package.tar.gz -P ./cache

# GloVe word vectors pre-trained on Twitter corpus
wget http://nlp.stanford.edu/data/glove.twitter.27B.zip -P ./cache

# Bataclan twitte corpus
#wget https://github.com/edupoux/MVA_2018_SL/raw/master/TD_%233/CorpusBataclan_en.1M.raw.txt.gz -P ./cache

# Decompress data files
mkdir ./models/c2v.mscc.model
mkdir ./models/c2v.ukwac.model
tar -xzvf cache/context2vec.mscc.model.package.tar.gz -C ./models/c2v.mscc.model
tar -xzvf cache/context2vec.ukwac.model.package.tar.gz -C ./models/c2v.ukwac.model
#gzip -d ./cache/CorpusBataclan_en.1M.raw.txt.gz
#mv ./cache/CorpusBataclan_en.1M.raw.txt ./corpus

# Dictionary files
#wget https://raw.githubusercontent.com/cbaziotis/ekphrasis/master/ekphrasis/dicts/noslang/manager.py -P ./dicts
#wget https://github.com/cbaziotis/ekphrasis/raw/master/ekphrasis/dicts/noslang/slangdict.pickle -P ./dicts
#wget https://github.com/dwyl/english-words/raw/master/words_alpha.txt -P ./dicts
