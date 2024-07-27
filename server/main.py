import joblib
import matplotlib.pyplot as plt
import io
class Model:
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
        model = joblib.load('server\\cardio_disease_prob')
        res.append(L[0]) # age index-0
        res.append(L[3]) # ap_hi index-1
        res.append(L[4]) # ap_lo index-2
        
        cholesterol = Model.cholesterolLevel(L[5])
        res.append(cholesterol) # cholesterol index-3
       
        glucose = Model.glucLevel(L[6])
        res.append(glucose)# gluc index-4
        
        BMI = Model.getBMI(L[1],L[2])
        res.append(BMI) # BMI   index-5
        
        result = model.predict_proba([res])
        # print(result[0,:])
        return round(result[0,1],3)

class Result:
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