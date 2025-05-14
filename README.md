# Heron Coding Challenge - File Classifier - Submission Notes

My approach at first started down the route of training a classifier then I relaised it would be possibly better to use OpenAI's API to do this instead. The main reason being that access to training data would be limited and if I was going use OpenAI to generate it then it made more sense to use it for the classifying.

I refactored the code to compact the logic into fewer functions while not overloading them. I moved the crucial logic to the classifier.py file too. My thinking was also that as the application grows it would be easier to leave app.py as the place where all the endpoints are clearly defined and have the logic in separate files for each endpoint. On this point as the application grows it would probably be a good idea to have different endpoints for different file type classifiers (e.g. one specifically for images, one for text docs, etc) as it would make it easier to write specialised logic to analyse and categorise just those functions. This would also allow different file types to be stored for processing more ooptimally as different endpoints could use different storage types (e.g. one type of temporary storage solution for images and another for text docs).

Along with the refactor I amended the tests too. Most notably I incorporated the provided test files into the testing.
