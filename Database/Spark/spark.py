# solutions.py

import pyspark
from pyspark.sql import SparkSession
import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt
from pyspark.ml.feature import StringIndexer, OneHotEncoderEstimator
from pyspark.ml.tuning import ParamGridBuilder, TrainValidationSplit
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator as MCE


# ---------------------------- Helper Functions ---------------------------- #

def plot_crime(data, category):
    """
    Helper function that plots the crime and income data from problem 4.
    Parameters:
        data ((n, 3) nparray, dtype=str (or '<U22')); format should be:
            First Column:   borough name
            Second Column:  crime rate (i.e. avg crimes per month)
            Third Column:   category (i.e. minor category) of crime
    Returns: None
    """
    domain = np.arange(len(data))
    fig, ax = plt.subplots()

    # plot number of months with
    p1 = ax.plot(domain, data[:, 1].astype(float) , color='red', label='Months w/ 1+ {}'.format(category))

    # create and plot on second axis
    ax2 = ax.twinx()
    p2 = ax2.plot(domain, data[:, 2].astype(float), color='green', label='Median Income')

    # create legend
    plots = p1 + p2
    labels = [line.get_label() for line in plots]
    ax.legend(plots, labels, loc=0)

    plt.title('Months w/ 1+ {} with Median Income'.format(category))

    plt.show()



# --------------------- Resilient Distributed Datasets --------------------- #

### Problem 1
def word_count(filename='data-files/huck_finn.txt'):
    """
    A function that counts the number of occurrences unique occurrences of each
    word. Sorts the words by count in descending order.
    Parameters:
        filename (str): filename or path to a text file
    Returns:
        word_counts (list): list of (word, count) pairs for the 20 most used words
    """
    # start the SparkSession
    spark = SparkSession.builder.appName("app_name").getOrCreate()

    # load the file as an RDD
    huck_finn = spark.sparkContext.textFile(filename)

    # count the number of occurances of each word
    pclass = huck_finn.flatMap(lambda row: row.split())
    pclass = pclass.map(lambda row: (row, 1))
    pclass = pclass.reduceByKey(lambda x, y: x + y)

    # sort the words by count, in descending order
    pclass = pclass.sortBy(lambda row: row[1], ascending=False).collect()

    # end the SparkSession
    spark.stop()

    # return a list of the (word,count) pairs for the 20 most used words
    return pclass[:20]

### Problem 2
def monte_carlo(n=10**5, parts=6):
    """
    Runs a Monte Carlo simulation to estimate the value of pi.
    Parameters:
        n (int): number of sample points per partition
        parts (int): number of partitions
    Returns:
        pi_est (float): estimated value of pi
    """
    # start the SparkSession
    spark = SparkSession.builder.appName("app_name").getOrCreate()

    # initialize an RDD with n*parts sample points and parts partitions
    sample = spark.sparkContext.parallelize(np.random.uniform(low=-1, high=1, size=(n*6, 2)), parts)
    num_inside = sample.filter(lambda row: np.linalg.norm(row) <= 1).count()
    percentage = num_inside / (n*6)

    # end the SparkSession
    spark.stop()

    # return your estimate
    return percentage * 4


# ------------------------------- DataFrames ------------------------------- #

### Problem 3
def titanic_df(filename='data-files/titanic.csv'):
    """
    Extracts various statistics from the titanic dataset. The dataset has the
    following structure:
    Survived | Class | Name | Sex | Age | Siblings/Spouses Aboard | Parents/Children Aboard | Fare
    Returns:
        """
    # start the SparkSession
    spark = SparkSession.builder.appName("app_name").getOrCreate()

    # load the dataset into a DataFrame
    schema = ('survived INT, pclass INT, name STRING, sex STRING, ' +
               'age FLOAT, sibsp INT, parch INT, fare FLOAT')
    titanic = spark.read.csv(filename, schema)

    # how many males/females onboard
    male_female = titanic.groupBy("sex").count()
    count = male_female.select("count").collect()

    # extract the female and male survival rates
    survived = titanic.groupBy("sex", "survived").count()
    survived = survived.select("count").collect()

    men_rate = survived[3][0] / (survived[0][0] + survived[3][0])
    women_rate = survived[1][0] / (survived[1][0] + survived[2][0])

    # end the SparkSession
    spark.stop()
    
    # return results
    return count[0][0], count[1][0], women_rate, men_rate 

### Problem 4
def crime_and_income(f1='data-files/london_crime_by_lsoa.csv',
                     f2='data-files/london_income_by_borough.csv', min_cat='Murder'):
    """
    Explores crime by borough and income for the specified min_cat
    Parameters:
        f1 (str): path to csv file containing crime dataset
        f2 (str): path to csv file containing income dataset
        min_cat (str): crime minor category to analyze
    returns:
        list: borough names sorted by percent months with crime, descending
    """
    # start the SparkSession
    spark = SparkSession.builder.appName("app_name").getOrCreate()

    # load the two files as PySpark DataFrames
    lsoa = spark.read.csv(f1, header=True, inferSchema=True)
    borough = spark.read.csv(f2, header=True, inferSchema=True)
    
    # create a new dataframe containing specified crime category
    crime = lsoa.join(borough, on="borough", how="inner")
    crime = crime.filter(crime.minor_category == min_cat)

    # Avg up the number of crimes each month for each borough
    crime = crime.groupBy("borough", "median-08-16").avg("value")

    # order dataframe by average crime rate, descending
    data = np.array(crime.sort("avg(value)", ascending=False).collect())
    
    # stop the SparkSession
    spark.stop()

    plot_crime(data, min_cat)

    return list(data[:, 0])

### Problem 5
def titanic_classifier(filename='data-files/titanic.csv'):
    """
    Implements a logistic regression to classify the Titanic dataset.
    Parameters:
        filename (str): path to the dataset
    Returns:
        lr_metrics (list): a list of metrics gauging the performance of the model
            ('f1', 'accuracy', 'weightedPrecision', 'weightedRecall')
    """
    # start the SparkSession
    spark = SparkSession.builder.appName("app_name").getOrCreate()

    # load the dataset into a DataFrame
    schema = ('survived INT, pclass INT, name STRING, sex STRING, ' +
               'age FLOAT, sibsp INT, parch INT, fare FLOAT')
    titanic = spark.read.csv(filename, schema)

    # vectorize the features
    sex_binary = StringIndexer(inputCol='sex', outputCol='sex_binary')
    onehot = OneHotEncoderEstimator(inputCols=['pclass'], outputCols=['pclass_onehot'])
    features = ['sex_binary', 'pclass_onehot', 'age', 'sibsp', 'parch', 'fare']
    features_col = VectorAssembler(inputCols=features, outputCol='features')

    pipeline = Pipeline(stages=[sex_binary, onehot, features_col])
    titanic = pipeline.fit(titanic).transform(titanic)

    titanic = titanic.drop('pclass', 'name', 'sex')

    # split test and train data
    train, test = titanic.randomSplit([0.75, 0.25], seed=11)

    # initialize classifier
    model = LogisticRegression(labelCol='survived', featuresCol='features')

    # train the model
    paramGrid = ParamGridBuilder().addGrid(model.elasticNetParam, [0, 0.5, 1]).build()
    tvs = TrainValidationSplit(estimator=model, estimatorParamMaps=paramGrid,
                                evaluator=MCE(labelCol='survived'), trainRatio=0.75, seed=11)
    clf = tvs.fit(train)

    # make predictions
    results = clf.bestModel.evaluate(test)

    # return metric values in order from above
    sol = results.accuracy, results.weightedRecall, results.weightedPrecision

    # stop the SparkSession
    spark.stop()

    return sol