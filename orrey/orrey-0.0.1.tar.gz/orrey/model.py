import matplotlib.pyplot as plt
import moss
import numpy as np
import os
import pandas as pd
import seaborn as sns
sns.set_style('white')


class ModelWrapper(object):
    def __init__(self, designs):
        '''Model Design Abstraction

        Inputs: designs: Either a pandas dataframe or a filename (or list of filenames)
        of onset design files (containign at least 'onset' and 'condition' columns)

        Properties:

        designFiles : List of Input Design File (or None if initialized w/ a
                         dataframe)
        * mat : Moss GLM Design
        * designDf : Pandas df rows are timepoints
        '''

        if isinstance(designs, pd.DataFrame):
            self.designFiles = None
            self.designDf = designs
            self._basename = None
        else:
            self.designFiles = designs
            designList = []
            runDur = None
            for i, designFile in enumerate(designs):
                runDf = pd.read_csv(designFile)
                if not runDur:
                    runDur = runDf['onset'].max()
                if 'run' in runDf.columns and len(runDf['run'].unique()) == 1:
                    # Assume 1-base run index and add total run duration
                    runDf['onset'] += runDur * (runDf['run'][0] - 1)
                designList.append(runDf)
            self.designDf = pd.concat(designList)
            self._basename = os.path.splitext(os.path.commonprefix(designs))[0]

        self.mat, self.design = self.buildDesign(self.designDf)
        self.corrFrame = self.buildCorrFrame()

    def buildDesign(self, df, tr=2):
        maxTime = int(df['onset'].max())
        ntp = maxTime / tr

        mat = moss.glm.DesignMatrix(design=df, ntp=ntp, tr=tr)
        design = mat.design_matrix

        # Remove zero-columns (runEnd)
        design = design[design.columns[(design != 0).any()]]

        return mat, design

    def _saveDesign(self, outfile=None):
        if not outfile:
            outfile = self.basename + '_designmatrix.csv'
        print('saving moss glm as csv matrix %s' % outfile)
        self.design.to_csv(outfile)

    def buildCorrFrame(self, cols=None):
        if not cols:
            cols = self.design.columns.values
        return pd.DataFrame(
            np.corrcoef(self.mat.design_matrix[cols].T),
            columns=cols,
            index=cols)

    def _saveFigure(self, outfile=None):
        fig, ax = plt.subplots(1, 2, figsize=(10, 5))

        # Plot Design Timeseries
        sns.heatmap(self.design,
                    cmap='gray',
                    yticklabels=False,
                    ax=ax[0],
                    cbar=False)
        ax[0].set_xticklabels(ax[0].xaxis.get_majorticklabels(), rotation=90)

        # Plot Correlation
        sns.heatmap(self.corrFrame, annot=True, ax=ax[1], cbar=True)
        plt.yticks(rotation=0)
        plt.xticks(rotation=90)
        plt.tight_layout()

        if not outfile:
            outfile = self.basename + '_Collinearity.png'

        fig.savefig(outfile)

    @property
    def basename(self):
        if self._basename:
            base = self._basename
        else:
            raise StandardError("No default basename for pandas dataframes")
        return base

    @basename.setter
    def basename(self, value):
        self._basename = value
