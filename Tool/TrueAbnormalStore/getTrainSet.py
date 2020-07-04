
import os
if __name__=="__main__":

    train_file = open("./train.txt","w")

    names = os.listdir("./Annotations")

    for name in names:
        train_file.write(name.split(".")[0]+"\n")
    train_file.close()
