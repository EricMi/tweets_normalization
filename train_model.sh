if [ "$#" -eq 2 ]
then
	python utils/clean_corpus.py $PWD $2 $1
python context2vec/train/corpus_by_sent_length.py $1
python context2vec/train/train_context2vec.py  -i "corpus/$1.DIR"  -w "$1.words"  -m "$1.model"  -c lstm  --deep yes  -t 3  --dropout 0.1  -u 300  -e 8  -p 0.75  -b 100  -g 0
