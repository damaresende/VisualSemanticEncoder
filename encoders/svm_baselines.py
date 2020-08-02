import json
from encoders.tools.src.svm_classification import SVMClassifier, DataType

n_folds = 5
result = {'i_cub': dict(), 'r_cub': dict(), 'i_awa': dict(), 'r_awa': dict()}

svm_cub = SVMClassifier(DataType.CUB)
vis_data, lbs_data, sem_data = svm_cub.get_data('../../../Datasets/SAE/cub_demo_data.mat')

result['i_cub']['sem'] = svm_cub.classify_sem_data(sem_data, lbs_data, n_folds)
result['i_cub']['vis'] = svm_cub.classify_vis_data(vis_data, lbs_data, n_folds, False)
result['i_cub']['cat'] = svm_cub.classify_concat_data(vis_data, sem_data, lbs_data, n_folds)
result['i_cub']['sae'] = svm_cub.classify_sae_data(vis_data, sem_data, lbs_data, n_folds)

vis_data, lbs_data, sem_data = svm_cub.get_data('../../../Datasets/SAE/cub_demo_data_resnet.mat')

result['r_cub']['sem'] = svm_cub.classify_sem_data(sem_data, lbs_data, n_folds)
result['r_cub']['vis'] = svm_cub.classify_vis_data(vis_data, lbs_data, n_folds, False)
result['r_cub']['cat'] = svm_cub.classify_concat_data(vis_data, sem_data, lbs_data, n_folds)
result['r_cub']['sae'] = svm_cub.classify_sae_data(vis_data, sem_data, lbs_data, n_folds)

svm_awa = SVMClassifier(DataType.AWA)
vis_data, lbs_data, sem_data = svm_awa.get_data('../../../Datasets/SAE/awa_demo_data.mat')

result['i_awa']['sem'] = svm_awa.classify_sem_data(sem_data, lbs_data, n_folds)
result['i_awa']['vis'] = svm_awa.classify_vis_data(vis_data, lbs_data, n_folds, False)
result['i_awa']['cat'] = svm_awa.classify_concat_data(vis_data, sem_data, lbs_data, n_folds)
result['i_awa']['sae'] = svm_awa.classify_sae_data(vis_data, sem_data, lbs_data, n_folds)


vis_data, lbs_data, sem_data = svm_awa.get_data('../../../Datasets/SAE/awa_demo_data_resnet.mat')

result['r_awa']['sem'] = svm_awa.classify_sem_data(sem_data, lbs_data, n_folds)
result['r_awa']['vis'] = svm_awa.classify_vis_data(vis_data, lbs_data, n_folds, False)
result['r_awa']['cat'] = svm_awa.classify_concat_data(vis_data, sem_data, lbs_data, n_folds)
result['r_awa']['sae'] = svm_awa.classify_sae_data(vis_data, sem_data, lbs_data, n_folds)

with open('baseline_result.json', 'w+') as f:
    json.dump(result, f, indent=4, sort_keys=True)