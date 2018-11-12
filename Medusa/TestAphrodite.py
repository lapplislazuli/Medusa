#For Test and Plot only
import matplotlib.pyplot as plt

import FeedAphrodite as FA
###### Plots and Tests #####

def plot_distribution(model,n=1000):
        plot_distribution_with_threshhold(model,0,n)

def plot_distribution_with_threshhold(model,threshhold,n=1000):
        scores, imgs = FA.create_and_rate_n_images(model,n)
        highscores = [FA.get_highest_score_and_class(s) for s in scores]
        threshholded = [c for c,a in highscores if a>threshhold]
        plt.hist(x=threshholded, bins=43)
        plt.grid(axis='y', alpha=0.75)
        plt.xlabel('Label')
        plt.ylabel('Frequency')
        plt.title('Label Distribution')
        plt.show()

def plot_distribution_with_compared_threshhold(model,threshhold,n=1000):
        scores, imgs = FA.create_and_rate_n_images(model,n)
        topscorer = [FA.get_highest_score_and_class(s) for s in scores]
        threshholded = [c for c,a in topscorer if a > threshhold]
        unthreshholded = [c for c,a in topscorer]
        plt.figure()
        plt.hist([unthreshholded,threshholded], 43)
        plt.xlabel('Label')
        plt.ylabel('Frequency')
        plt.title('Label Distribution')
        plt.show()

def plot_prop_dist(model,n=1000):
        scores, imgs = FA.create_and_rate_n_images(model,n)
        topscorer = []
        for s in scores:
                c,a = FA.get_highest_score_and_class(s)
                topscorer.append(a)
        plt.hist(topscorer, bins=100, normed='density')
        plt.xlabel('Prop')
        plt.ylabel('Frequency')
        plt.title('Propability Distribution')
        plt.show()

def plot_prop_dist_of_label(model,label,n=1000):
        scores, imgs = FA.create_and_rate_n_images(model,n)
        labelScores = [s[label] for s in scores]
        plt.hist(labelScores, bins=20, normed='density')
        plt.xlabel('Prop')
        plt.ylabel('Frequency')
        plt.title('Propability Distribution')
        plt.show()

def plot_all_scores(model,n=1000):
        #Not Really Human Readable, but maybe Someone can improve?
        scores, imgs = FA.create_and_rate_n_images(model,n)
        plt.hist(scores, bins=5, normed='density')
        plt.xlabel('Prop')
        plt.ylabel('Frequency')
        plt.title('Propability Distribution')
        plt.show()