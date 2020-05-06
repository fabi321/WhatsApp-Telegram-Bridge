```
mkdir mozilla
cd mozilla
```
Go to [Mozilla Common Voice](https://voice.mozilla.org/de/datasets) and download the file.  
Move it to PROJECT_DIRECTORY/mozilla/
```
tar -xzf de.tar.gz
rm de.tar.gz
mkdir tuda
cd tuda
wget http://ltdata1.informatik.uni-hamburg.de/kaldi_tuda_de/german-speechdata-package-v2.tar.gz
tar -xzf german-speechdata-package-v2.tar.gz
rm german-speechdata-package-v2.tar.gz
wget http://ltdata1.informatik.uni-hamburg.de/kaldi_tuda_de/German_sentences_8mil_filtered_maryfied.txt.gz
gzip -d German_sentences_8mil_filtered_maryfied.txt.gz
cd ..
git clone https://github.com/mozilla/DeepSpeech.git
. venv/bin/activate
pip3 install -r DeepSpeech/requirements.txt
pip3 install $(python3 DeepSpeech/util/taskcluster.py --decoder)
```
recommendation:
```
pip3 uninstall tensorflow
pip3 install 'tensorflow-gpu==1.14.0'
```
make sure you have vox with mp3 support for Ubuntu: ```sudo apt install libsox-fmt-mp3```  
afterwards:
```
DeepSpeech/bin/import_cv2.py --filter_alphabet alphabet.txt mozilla
python3 convert_tuda_to_csv.py
cd mozilla/clips
python3 /home/fabian/WhatsApp-Telegram-Bridge/check_wav_files.py -check-length
cd ../../
DeepSpeech/DeepSpeech.py --train_files mozilla/clips/train.csv --dev_files mozilla/clips/dev.csv --test_files mozilla/clips/test.csv --automatic_mixed_precision=True --alphabet_config_path=alphabet.txt
```
