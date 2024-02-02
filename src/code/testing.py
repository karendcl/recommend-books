import trial
import pickle

trial.Load_First_Time()

#load model
with open('lda_model.pkl', 'rb') as f:
    model1 = pickle.load(f)

#add new document
trial.Add_New_Document('This is a document that should be related to the eighteenth century and the french revolution', 'French Revolution')

#load model
with open('lda_model.pkl', 'rb') as f:
    model2 = pickle.load(f)

#compare the two models
assert model1 != model2

data = trial.Add_New_Document('This is a document that should be related to the eighteenth century and the french revolution', 'French Revolution 7 ')

print(trial.make_suggestion([0,2,5]))