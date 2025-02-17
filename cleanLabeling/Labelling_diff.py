import numpy as np
from sklearn.externals import joblib
import os
from DrumReducerExpander import DrumReducerExpander
class Labelling:

    def __init__(self,filepath_dataset,filepath_tags):


        self.filepath_dataset = filepath_dataset
        self.filepath_tags = filepath_tags


    def macro_iteration(self):


        # ITERATE OVER THE TAG LISTS

        for tag_i, tag in enumerate(self.filepath_tags):


            print('>>' + tag[29:-3])
            with open(tag, 'r') as f:
                # ITERATE OVER THE FOLDER LISTS

                for i, file in enumerate(f):
                    # (str(f))
                    #                 print('load files..{}/{}'.format(i + 1, number_files[tag_i]), end="\r")
                    self.file = file.rstrip()
                    self.middle = '/'.join(self.file[2:5]) + '/'
                    p = self.filepath_dataset + self.middle + self.file

                    for npz in os.listdir(p):
                        if '_metadata_training' in npz:
                            self.label(p,npz)


    def label(self,path,npz):

        data=dict(np.load(path+'/'+npz))
        rdv=(data['reduced_drums_velocity']>0)*1
        rdv=rdv.reshape((rdv.shape[0],-1))
        diff=np.stack((rdv[:-2,:],rdv[1:-1],rdv[2:]),axis=1)
        diff1=np.sum((diff[:, 1, :] - diff[:, 0, :]>0)*1,axis=1)
        diff2 = np.sum((diff[:, 1, :] - diff[:, 2, :] > 0) * 1, axis=1)
        y=(np.logical_and(diff1>10,diff2>10))*1
        # print(y.shape)
        y=np.concatenate(([0],y,[0]))
        np.savez(path+'/' + npz.replace('_metadata_training.npz','') + '_label_diff_10.npz', label=y)



    def predict(self,data):
        pass

        # dataset=DnnDataset(data,[],downsampling=False,upsampling=False,inference=True)
        # inference_loader = torch.utils.data.DataLoader(dataset=dataset, batch_size=len(dataset),shuffle=False)
        # y_pred_total = []
        # with torch.no_grad():
        #     for i, (X_deep) in enumerate(inference_loader):
        #         X_d = Variable(X_deep).float()
        #         y_pred = self.model(X_d)
        #         y_pred_cat = (y_pred >0.5).squeeze(1).float()
        #
        #         y_pred_total.append(tensor_to_numpy(y_pred_cat).astype(int))
        #
        #
        # y_pred_total = np.concatenate(y_pred_total)


        # return y_pred_total







if __name__=='__main__':
    PATH = '//home/ftamagna/Documents/_AcademiaSinica/dataset/lpd_debug/'
    PATH_TAGS = [
        '/home/ftamagna/Documents/_AcademiaSinica/code/LabelDrumFills/id_lists/tagtraum/tagtraum_Rock.id',
    ]

    lb=Labelling(PATH,PATH_TAGS)
    lb.macro_iteration()

