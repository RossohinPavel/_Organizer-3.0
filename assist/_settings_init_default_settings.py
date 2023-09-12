import pickle


with open('../data/settings.pcl', 'wb') as file:
    pickle.dump({'autolog': False, 'log_check_depth': 1, 'autofile': False, 'z_disc': '', 'o_disc': '', 't_disc': ''}, file)
