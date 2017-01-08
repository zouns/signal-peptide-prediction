import parse
import matplotlib.pyplot as plt
import sys
import numpy as np

def cleavage_position_hist(data):
	cleavage_positions = []
    
	for sample in data:
		cleavage_positions += [sample['annotationLine'].index('C')]
    
	plt.hist(cleavage_positions, color='c')
	plt.xlabel('Cleavage position')
	plt.ylabel('Nb of training sample')
	plt.show()

def get_peptides(data):
	# print len(data)
	peptide_aa_seqs = []
	for sample in data:
		cleav = len(sample['annotationLine'].split('C')[0])
		# print cleav
		peptide_aa_seq = sample['sequence'][0:cleav]
		# print peptide_aa_seq
		peptide_aa_seqs += [peptide_aa_seq]
	# print peptide_aa_seqs
	# print len(data)
	# print len(peptide_aa_seqs)
	# peptide_aa_seqs = np.array(peptide_aa_seqs)
	indices = []
	for seq in peptide_aa_seqs:
		indices += [[idx,aa] for (idx,aa) in enumerate(seq)]
	aa_dir = {}
	for x in indices:
		if x[1] not in aa_dir:
			aa_dir[x[1]] = []
		aa_dir[x[1]] += [x[0]]

	colormap = plt.cm.Set1 #I suggest to use nipy_spectral, Set1,Paired
	plt.gca().set_color_cycle([colormap(i) for i in np.linspace(0, 1,20)])
	plt.hist(aa_dir.values(), bins=62, histtype='bar', stacked=True, label=aa_dir.keys())
	plt.legend()
	plt.xlabel('position')
	plt.ylabel('Nb of each AA at this position')
	plt.show()


# def aa_repartition(data):


if __name__ == '__main__':

	if len(sys.argv) <= 1 or sys.argv[1] not in ["tm","nontm","all"]:
	    sys.stderr.write("You need to choose a correct mode :\ntm\nnontm\nall\n")
	    sys.exit("Script exited with error")
	
	else:
	    mode = sys.argv[1]
	    if len(sys.argv) == 2:
	        print ("Default training proportion chosen : 0.7")
	        trainingProportion = 0.7
	    else:    
	        trainingProportion = float(sys.argv[2])
	        if not (trainingProportion <= 1.0 and trainingProportion >= 0):
	            sys.stderr.write("The proportion should be between 0 and 1\n")
	            sys.exit("Script exited with error")

	    data = parse.accessFolders(mode, trainingProportion)

	    trainingdata = []
	    peptide_trainingdata = []
	    for sample in data:
	    	if sample['isTraining']=='y':
	    		trainingdata += [sample]
	    		if sample['label']=='p':
	    			peptide_trainingdata += [sample]	

	    # cleavage_position_hist(peptide_visudata)
	    get_peptides(peptide_trainingdata)