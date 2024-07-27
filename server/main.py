import joblib
import tensorflow as tf
import matplotlib.pyplot as plt
import io
import numpy as np

# Covid Model
class Covid_Model:
    def predict( self , images):
        model = tf.keras.models.load_model("./server/covid19_CNN")
        class_names = ["covid" , "Normal" , "Viral Pneumonia"]
        #plt.imshow(images)
        # Optionally, resize the image
        predicted_class_names = []
        # Ensure the batch size is 32
        if images.shape[0] < 32:
            images = np.tile(images, (32 // images.shape[0] + 1, 1, 1, 1))[:32]

        print(images.shape)
        prediction = model.predict(images)
        
        for indices in prediction:
            index = np.argmax(indices)
            class_name = class_names[index]
            predicted_class_names.append(class_name)
        #print(predicted_class_names[0])
        return predicted_class_names[0]

# Covid model image generator
class Image_generator:
    def generate_images(self , image):
       # image = tf.image.resize(image, [180, 180])
       # image = tf.expand_dims(image, axis=0)
        images = []
        
        datagen = tf.keras.preprocessing.image.ImageDataGenerator(
                rotation_range=0,
                width_shift_range=0,
                height_shift_range=0,
                shear_range=0,
                zoom_range=0,
                horizontal_flip=False,
                fill_mode='nearest'
            )
        image_gen = datagen.flow(image, batch_size=1)

        # Generate and store images
        for _ in range(5):
            generated_image = image_gen.next()
            images.append(generated_image[0])
            
        images = np.array(images)
        
        return images

# cardiac Model
class Cardiac_Model:
    # get cholesterol
    def cholesterolLevel(value):
        if(value<200):
            return 0
        elif value>=200 and value<=239:
            return 1
        else:
            return 2
    # get glucose level
    def glucLevel(value):
        if value>=70 and value<100:
            return 0
        elif value>=100 and value<126:
            return 1
        else:
            return 2
    
    def getBMI(hight,weight):
        return (weight)/(hight*hight)
    
    def predict(L):
        res = []
        # model_path = os.path.join('sever','cardio_disease_prob')
        model = joblib.load('./server/cardio_disease_prob')
        res.append(L[0]) # age index-0
        res.append(L[3]) # ap_hi index-1
        res.append(L[4]) # ap_lo index-2
        
        cholesterol = Cardiac_Model.cholesterolLevel(L[5])
        res.append(cholesterol) # cholesterol index-3
       
        glucose = Cardiac_Model.glucLevel(L[6])
        res.append(glucose)# gluc index-4
        
        BMI = Cardiac_Model.getBMI(L[1],L[2])
        res.append(BMI) # BMI   index-5
        
        result = model.predict_proba([res])
        # print(result[0,:])
        return round(result[0,1],3)


class Cardiac_image_Result:
    def get_image(value):
        color=""
        title = ""
        if value<0.34:
            color="green"
            title = "perfect, no danger"
        elif value<0.68 and value>=0.34:
            color="orange"
            title = "suggested to take precaution"
        elif value<1 and value>=0.68:
            color="red"
            title = "Better consult a doctor"
        fig, ax = plt.subplots()
        ax.barh(['prediction'], [value], color=color)
        ax.set_xlim(0, 1)  # Set x-axis range from 0 to 1
        ax.set_xlabel('severity')
        ax.set_title(title)
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close(fig)

        return buf
# print(Model.predict([59,151,67,120,80,1,1]))
