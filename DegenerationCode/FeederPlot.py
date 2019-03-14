#For Test and Plot only
import matplotlib.pyplot as plt
import numpy as np

import Feeder as Feeder
import LabelDictionary as labDict
###### Plots and Tests #####

def plot_distribution(model,n=1000):
        plot_distribution_with_threshhold(model,0,n)

def plot_distribution_with_threshhold(model,threshhold,n=1000):
        scores, imgs = Feeder.create_and_rate_n_images(model,n)
        highscores = [Feeder.get_highest_score_and_class(s) for s in scores]
        threshholded = [c for c,a in highscores if a>threshhold]
        plt.hist(x=threshholded, bins=43)
        plt.grid(axis='y', alpha=0.75)
        plt.xlabel('Label')
        plt.ylabel('Frequency')
        plt.title('Label Distribution')
        plt.show()

def plot_distribution_with_compared_threshhold(model,threshhold,n=1000):
        scores, imgs = Feeder.create_and_rate_n_images(model,n)
        topscorer = [Feeder.get_highest_score_and_class(s) for s in scores]
        threshholded = [c for c,a in topscorer if a > threshhold]
        unthreshholded = [c for c,a in topscorer]
        plt.figure()
        plt.hist([unthreshholded,threshholded], 43)
        plt.xlabel('Label')
        plt.ylabel('Frequency')
        plt.title('Label Distribution')
        plt.show()

def plot_prop_dist(model,n=1000):
        scores, imgs = Feeder.create_and_rate_n_images(model,n)
        topscorer = []
        for s in scores:
                c,a = Feeder.get_highest_score_and_class(s)
                topscorer.append(a)
        plt.hist(topscorer, bins=100, normed='density')
        plt.xlabel('Prop')
        plt.ylabel('Frequency')
        plt.title('Propability Distribution')
        plt.show()

def plot_prop_dist_of_label(model,label,n=1000):
        scores, imgs = Feeder.create_and_rate_n_images(model,n)
        labelScores = [s[label] for s in scores]
        plt.hist(labelScores, bins=20, normed='density')
        plt.xlabel('Prop')
        plt.ylabel('Frequency')
        plt.title('Propability Distribution')
        plt.show()

def plot_all_scores(model,n=1000):
        #Not Really Human Readable, but maybe Someone can improve?
        scores, imgs = Feeder.create_and_rate_n_images(model,n)
        plt.hist(scores, bins=5, density=True)
        plt.xlabel('Prop')
        plt.ylabel('Frequency')
        plt.title('Propability Distribution')
        plt.show()

#Helper for bar chart
def autolabel(rects, ax, xpos='center'):
        """
        Attach a text label above each bar in *rects*, displaying its height.

        *xpos* indicates which side to place the text w.r.t. the center of
        the bar. It can be one of the following {'center', 'right', 'left'}.
        """

        xpos = xpos.lower()  # normalize the case of the parameter
        ha = {'center': 'center', 'right': 'left', 'left': 'right'}
        offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                    '{}'.format(height), ha=ha[xpos], va='bottom')

def plot_comparison_trasi_aphrodite_score(trasi_score, aphrodite_score):
        trasi_plot_scores = []
        aphrodite_plot_scores = []
        xlabels = []
        for i in range(len(trasi_score)):
                indexFromGermanGTSRBClass = int(labDict.GTSRB_GERMAN_LABEL_TO_INT[trasi_score[i]['class']])
                trasi_plot_scores.append(trasi_score[i]['confidence'])
                aphrodite_plot_scores.append(aphrodite_score[0][indexFromGermanGTSRBClass])
                xlabels.append(i)
        print(trasi_plot_scores)
        print(aphrodite_plot_scores)
        ind = np.arange(len(trasi_plot_scores)) #x locations for the group
        width = 0.35 # width of bars
        fig, ax = plt.subplots()
        rects1 = ax.bar(ind - width/2, trasi_plot_scores, width,
                color='SkyBlue', label='Trasi Score')
        rects2 = ax.bar(ind + width/2, aphrodite_plot_scores, width,
                color='IndianRed', label='Aphrodite Score')
        ax.set_ylabel('Score')
        ax.set_title('Comparison of Trasi and Aphrodite Score per Class')
        ax.set_xticks(ind)
        ax.set_xticklabels(xlabels)
        ax.legend()
        
        #autolabel(rects1, ax, "left") Uncomment, if you need exact data, turned off by deFeederult, cause it is confusing
        #autolabel(rects2, ax, "right")
        plt.show()
