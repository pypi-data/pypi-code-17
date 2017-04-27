'''
Helper module to resample an EMC model (or directory) based on a new value
for ticksPerQuarterNote.

@author Csaba Sulyok
'''

from numpy import append, diff, arange, histogram, argmax, log2

from emc.core.integ.modeldir import ModelDirectory


class ModelResampler(object):
    '''
    Helper module to resample an EMC model (or directory) based on a new value
    for ticksPerQuarterNote.
    '''
    
    def findOptimalTicksPerQuarterNote(self, model):
        '''
        Given a model, finds optimal value for ticksPerQuarterNote, so that minimal quantization error occurs.
        Needed since many MIDIs are encoded with 384 ticks per quarter note, where the actual quarter notes are different sized.
        '''
        iois = model.interonsets()
        # find histogram of inter-onset intervals
        h = histogram(iois, bins=arange(max(iois)))[0]
        # discard notes occuring at the same time
        h[0] = 0
        # most occuring inter-onset interval
        maxioi = argmax(h)
        # find which note this should correspond to: quarter, eighth etc.
        # i.e. find n where (2^n * maxioi) closest to original ticksPerQuarterNote
        n = log2(float(model.ticksPerQuarterNote) / maxioi)
        # new ticksPerQuarterNote should be |2^n| * maxioi
        return round(2 ** n) * maxioi
    
    
        
    def resample(self, model, ticksPerQuarterNote):
        '''
        Assign new ticksPerQuarterNote, quantize data in a model.
        '''
        optimalTicks = self.findOptimalTicksPerQuarterNote(model)
        model.ticksPerQuarterNote = optimalTicks
        
        # calculate scaling factor
        q = float(ticksPerQuarterNote) / float(model.ticksPerQuarterNote)
        
        model.ticksPerQuarterNote = ticksPerQuarterNote
        model.length = 0
        
        for track in model.tracks:
            # scale down start and end times
            track.notes[:,2] *= q
            track.notes[:,3] *= q
            # deduce onset/duration from start and end time
            track.notes[:,1] = track.notes[:,3] - track.notes[:, 2]
            track.notes[:,0] = diff(append([0], track.notes[:,2]))
            
            if track.length != 0:
                track.length = sum(track.notes[:,0]) + track.notes[-1,1]
            model.length = max(track.length, model.length)
        
        return model
    
    
    def resampleDirectory(self, modelDir, ticksPerQuarterNote):
        '''
        Performs quantizations for each model within an instance of ModelDirectory.
        '''
        for i, model in enumerate(modelDir.models):
            modelDir.models[i] = self.resample(model, ticksPerQuarterNote)


'''
default instance and methods
'''
resampler = ModelResampler()
resample = resampler.resample
resampleDirectory = resampler.resampleDirectory


def resampleBachMidis():
    md = ModelDirectory('../../../../../midi/bach_original')
    
    # resampling - shortest note becomes 16th note
    resampleDirectory(md, 4)
    
    md.write('../../../../../midi/bach_1track', includeEmptyTracks = False)


if __name__ == '__main__':
    resampleBachMidis()