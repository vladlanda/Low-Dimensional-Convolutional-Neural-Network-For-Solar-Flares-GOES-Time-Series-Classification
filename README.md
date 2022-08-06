"Low Dimensional Convolutional Neural Network For Solar Flares GOES Time Series Classification" paper source code.

instructions:

1. Download the available data ranging from 1998 to 2019 at https://satdat.ngdc.noaa.gov/sem/goes/data/avg/ and place it in data/avg/ folder.
2. Execute source/goes_avg_preprocess.py for preprocessing, it will populate data/xray_avg_1m_numpy_data with preprocessed numpy files.
3. Go though source/keras_cnn_gru_geos_15.ipynb to train and evaluate the models.
	3.1 Tab 1  : Change PREDICTION_TIME_GAP = 60 * 72 for different predictions time frames.
	3.2 Tab 22 : Uncomment the preferred class model data X/M.
	3.3 Tab 23 : Uncomment the preferred data split.
	3.4 Tab 47 : Alternate between 1 and 0 for training.
	3.5 Tabs 54,55,56 : Loading models weight and evaluate the performance (tab 56 alternate between 1 and 0 for saving the evaluation data).
4. For pre-trained model download the zip from : https://drive.google.com/file/d/1AvpZ8wmVymDaOgFIohOvho4LdaG42_A_/view?usp=sharing and extract it's content into source/keras_models

Check more details here : [www.vladlanda.com](https://www.vladlanda.com/low-dimensional-convolutional-neural-network-for-solar-flares-goes-time-series-classification)
