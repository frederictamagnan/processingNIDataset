from TrainingSketchRnn import TrainingSketchRnn

LR=0.001

N_EPOCHS=300
for beta in [500]:
    for name,batch_size in [('Four',300)]:
        BATCH_SIZE=batch_size
        local_dataset='/home/ftamagnan/dataset/FillsExtracted'+name+'_cc.npz'

        tg=TrainingSketchRnn(lr=LR,batch_size=BATCH_SIZE,n_epochs=N_EPOCHS,dataset_filepath=local_dataset,beta=beta,linear_hidden_size=[64,32],gru_hidden_size=64)
        tg.load_data()
        tg.split_data()
        tg.train_model()
        tg.save_model("./../models/",'sketchrnn_'+name+'_'+str(beta)+'_v2.pt')