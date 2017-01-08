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
	plt.hist(aa_dir.values(), bins=500, histtype='bar', stacked=True, label=aa_dir.keys())
	plt.legend()
	plt.xlim([0,60])
	plt.xlabel('position')
	plt.ylabel('Nb of each AA at this position')
	plt.show()


def result_plot(result):
	plt.plot(result[:,0], result[:,1])
	max_y = max(result[:,1])  # Find the maximum y value
	max_x = result[:,0][result[:,1].argmax()]
	plt.xlabel('Nb of Amino Acid considered')
	plt.ylabel('Score')
	plt.text(max_x, max_y, '%i , %.2f'%(max_x,max_y))
	plt.show()


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
	    nonpeptide_trainingdata = []
	    for sample in data:
	    	if sample['isTraining']=='y':
	    		trainingdata += [sample]
	    		if sample['label']=='p':
	    			peptide_trainingdata += [sample]
	    		else:
	    			nonpeptide_trainingdata += [sample]

	    # cleavage_position_hist(peptide_visudata)
	    # get_peptides(peptide_trainingdata)
	    # get_peptides(nonpeptide_trainingdata)
	    all_result = np.array([[1, 0.68205128205128207], [3, 0.7384615384615385], [5, 0.71794871794871795], [7, 0.74102564102564106], [9, 0.80769230769230771], [11, 0.84358974358974359], [13, 0.84743589743589742], [15, 0.84358974358974359], [17, 0.88846153846153841], [19, 0.88461538461538458], [21, 0.86923076923076925], [23, 0.88205128205128203], [25, 0.85897435897435892], [27, 0.86410256410256414], [29, 0.84743589743589742], [31, 0.84999999999999998], [33, 0.82692307692307687], [35, 0.8371794871794872], [37, 0.77051282051282055], [39, 0.81282051282051282], [41, 0.80512820512820515], [43, 0.79358974358974355], [45, 0.78974358974358971], [47, 0.78205128205128205], [49, 0.7615384615384615], [51, 0.77051282051282055], [53, 0.77307692307692311], [55, 0.76282051282051277], [57, 0.75128205128205128], [59, 0.77820512820512822]])
	    result_plot(all_result)