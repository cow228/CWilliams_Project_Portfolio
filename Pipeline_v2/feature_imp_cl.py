import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype
from sklearn.feature_selection import mutual_info_classif, chi2, f_classif, mutual_info_regression
from scipy.stats import pearsonr
import dcor
from pandas.api.types import is_numeric_dtype
import matplotlib.pyplot as plt
import numpy as np
import textwrap

class Data_features:
    def __init__(self, dataframe, target):
        dataframe.columns = dataframe.columns.str.replace(' ', '_')
        self.data = dataframe.reset_index(drop=True)
        self.target = target
        self.features = [col.replace(' ', '_') for col in self.data.columns if col != self.target]
        self.numeric_features = self.data[self.features].select_dtypes(include='number').columns.tolist()
        self.categorical_features = self.data[self.features].select_dtypes(exclude='number').columns.tolist()
        self.binary_features = [col for col in self.features if self.data[col].nunique() == 2]
        self.multiclass_features = [col for col in self.categorical_features if col not in self.binary_features]
        self.target_correlations = None

        # Determine target type
        self.target_type = 'numeric' if is_numeric_dtype(self.data[self.target]) else 'categorical'
        if self.data[self.target].nunique() <= 5:
            self.target_type = 'categorical'
        if self.data[self.target].nunique() == 2:
            self.target_type = 'binary'

        # execute default functions to create additional attributes
        self._poly_feature_selection() # returns self.poly_features (used to identify polynomial and interaction for use in feature selection)
        self._bin() # returns self.binned_data
        # self._svd() # returns self.svd_data, self.svd_features, self.svd_ftr_importance
        self._svd_filter()
        self._dt_feature_selection() # returns self.dt_feature_importance
        
        # use all collected information to find most important features
        self._target_correlation() # returns self.target_correlations

    def _bin(self, bins = 4):
        features = [col for col in self.features if col not in self.poly_features_list]
  
        df = self.data.copy()
        binned_df = self.data[features].copy()
        
        for col in df[features].select_dtypes(include='number').columns:
            # Bin into quartiles and label them 1–4
            binned_df[col] = pd.qcut(df[col], q=4, labels=[1, 2, 3, 4])

        # binned_df.drop(self.target,axis=1, inplace=True)
        
        self.binned_features = [col+'_quarts' for col in binned_df.columns]

        binned_df.columns = self.binned_features
        for col in binned_df.columns:
            binned_df[col] = binned_df[col].astype('category')
        
        self.binned_data = binned_df

        self.data[binned_df.columns] = binned_df
        self.features.extend(binned_df.columns)
        self.multiclass_features.extend(binned_df.columns)
        self.categorical_features.extend(binned_df.columns)
    
    def _target_correlation(self, top_n = 15, pval_zero = False):
        # option to use alternate features, like SVD
        features = self.svd_filter_df['Feature'].to_list()
        feature_data = self.data
        target_data = self.data[self.target]

        def mi_clf_discrete_ft(col):
            mi = mutual_info_classif(feature_data[col].to_numpy().reshape(-1, 1), target_data.astype('category'), discrete_features=True)
            return mi
        def mi_clf_continuous_ft(col):
            mi = mutual_info_classif(feature_data[col].to_numpy().reshape(-1, 1), target_data.astype('category'), discrete_features=False)
            return mi
        def mi_reg_discrete_ft(col):
            mi = mutual_info_regression(feature_data[col].to_numpy().reshape(-1, 1), target_data, discrete_features=True)
            return mi
        def mi_reg_continuous_ft(col):
            mi = mutual_info_regression(feature_data[col].to_numpy().reshape(-1, 1), target_data, discrete_features=False)
            return mi
        def chi_square(col):
            f, p = chi2(feature_data[col].to_numpy().reshape(-1, 1), target_data.astype('category'))
            # return 1-p value for compound calculation, return 0 if option selected and p > 0.05
            if pval_zero:
                return [1-p[0] if p[0] < 0.05 else 0]
            else:
                return [1-p[0]]
        def anova(col): 
            # set the categorical value to the target
            target = target_data
            feature = feature_data[col].to_numpy().reshape(-1, 1)
            if self.target_type == 'numeric':
                target = feature_data[col].to_numpy().reshape(-1, 1)
                feature = target_data
            f, p = f_classif(feature, target)
            # return 1-p value for compound calculation, return 0 if option selected and p > 0.05
            # if pval_zero:
            #     return [1-p[0] if p[0] < 0.05 else 0]
            # else:
            #     return [1-p[0]]
            return f
        def dcorr(col):
            dcor_val = dcor.distance_correlation(feature_data[col], target_data)
            return dcor_val
        def lift(col):
            lift = 0
            n = len(feature_data)
            p_y = target_data.sum() / n
            p_x = feature_data[col].sum() / n
            p_xy = ((feature_data[col] == 1) & (target_data == 1)).sum() / n
            if p_x > 0 and p_y > 0:
                lift = p_xy / (p_x * p_y)
            return lift
        def corr(col):
            corr, _ = pearsonr(feature_data[col].to_numpy().reshape(-1, 1), target_data)
            return corr
        def test_list(col):
            feature_type = 'numeric'
            if col in self.binary_features: feature_type = 'binary'
            if col in self.multiclass_features: feature_type = 'categorical'

            possible_target_tests = {
                'binary' : {mi_clf_discrete_ft, mi_clf_continuous_ft, chi_square, lift},
                'categorical' : {mi_clf_discrete_ft, mi_clf_continuous_ft, chi_square},
                'numeric' : {mi_reg_discrete_ft, mi_reg_continuous_ft, dcorr, corr}
            }
            possible_feature_tests = {
                'binary' : {mi_clf_discrete_ft, mi_reg_discrete_ft, chi_square, lift},
                'categorical' : {mi_clf_discrete_ft, mi_reg_discrete_ft, chi_square},
                'numeric' : {mi_clf_continuous_ft, mi_reg_continuous_ft, dcorr, corr}
            }
            anova_test = {}
            if self.target_type == 'numeric' and feature_type in ['categorical', 'binary']: anova_test = {anova}
            if self.target_type in ['categorical', 'binary'] and feature_type == 'numeric': anova_test = {anova}

            tests = possible_target_tests[self.target_type].intersection(possible_feature_tests[feature_type])
            tests = tests.union(anova_test)

            return tests

        correlations = {}
        for col in features:
            correlations[col] = {}
            for test in test_list(col):
                correlations[col][test.__name__] = test(col)[0]

            correlations[col]['svd_importance'] = self.svd_filter_df.loc[self.svd_filter_df['Feature'] == col, 'Importance'].values[0]
            correlations[col]['dt_importance'] = self.dt_feature_importance.loc[self.dt_feature_importance['Feature'] == col, 'Importance'].values[0]


        # turn dict into dataframe
        correlations = pd.DataFrame(correlations).T

        # normalize all columns to 0-1 scale
        for col in correlations.columns:
            correlations[col] = (correlations[col] - correlations[col].min()) / (correlations[col].max() - correlations[col].min())

        # calculate mean of all (non nan) corelation features
        correlations['compound_correlation'] = correlations.mean(axis=1, numeric_only=True)

        # combine mutual information values into one column
        mi_cols = [col for col in correlations.columns if col.startswith('mi_')]
        if len(mi_cols)>0:
            correlations['mi'] = 0
            for mi_col in mi_cols:
                correlations[mi_col].fillna(0,inplace=True)
                correlations['mi'] = correlations['mi'] + correlations[mi_col]
                correlations.drop(mi_col, axis=1, inplace=True)

        stat_tests = [col for col in correlations.columns if col in ['anova', 'chi_square']]
        if len(stat_tests)>0:
            correlations['anova/chi'] = 0
            for stat_col in stat_tests:
                correlations[stat_col].fillna(0, inplace=True)
                correlations['anova/chi'] = correlations['anova/chi'] + correlations[stat_col]
                correlations.drop(stat_col, axis=1, inplace=True)

        self.target_correlations = correlations.sort_values(by='compound_correlation', ascending=False)
        return self

    def plot_target_correlation(self, top_n = 10, pval_zero = True, svd = False):
        plt.figure(figsize=(14, 5))
        
        # Get top N features
        plot_data = self.target_correlations.head(top_n)
        
        # Setup for bar chart
        wrap_lables = [textwrap.fill(label, width=16) for label in plot_data.index]
        wrap_lables = [label.replace(" ", "\nx\n") for label in wrap_lables]
        features = wrap_lables
        # features = plot_data.index
        correlation_types = [col for col in plot_data.columns if col != 'compound_correlation']
        
        # Calculate positions for grouped bars
        x = np.arange(len(features))
        width = 0.8 / len(correlation_types)  # Width of bars with spacing
        
        # Plot bars for each correlation type
        for i, column in enumerate(correlation_types):
            offset = (i - len(correlation_types)/2 + 0.5) * width
            plt.bar(x + offset, plot_data[column], width=width, label=column, alpha=0.5)
        
        # Plot compound correlation as a line
        plt.plot(x, plot_data['compound_correlation'], 'o-', linewidth=3, 
                 label='compound_correlation', markersize=8, color='black')
        
        plt.xticks(x, features, rotation=0)
        plt.xlabel('Features')
        plt.ylabel('Correlation Value')
        plt.title(f'Top {top_n} Features by Correlation with Target')
        plt.legend(loc='best')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        plt.show()

        return self
    
    def _svd(self):  # decomissioned in favor of SVD filter
        from sklearn.decomposition import TruncatedSVD

        svd = TruncatedSVD(n_components=len(self.features))
        svd.fit(self.data[self.features])
        cum_var = np.cumsum(svd.explained_variance_ratio_)
        k = np.argmax(cum_var >= 0.90) + 1
        # print(svd.singular_values_)

        svd = TruncatedSVD(n_components=k)
        svd.fit(self.data[self.features])
        self.svd_features = ['svd_' + str(k) for k in range(k)]
        self.svd_data = pd.DataFrame(svd.transform(self.data[self.features]), columns=self.svd_features)

        # sum absolute values of components for each feature
        self.svd_ftr_importance = pd.DataFrame({'Feature': self.features, 'Importance': np.abs(svd.components_).sum(axis=0)}).sort_values(by='Importance', ascending=False)

        return self

    def _dt_feature_selection(self):
        from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
        from sklearn.inspection import permutation_importance
        import random

        features = self.svd_filter_df['Feature'].to_list()

        if self.target_type in ['categorical', 'binary']:
            dt = DecisionTreeClassifier(random_state=0)
            target = self.data[self.target].astype('category')
        else: 
            dt = DecisionTreeRegressor(random_state=0)
            target = self.data[self.target]
   

        # create 5 training sets: mimicing random forest
        result_dict = {col: [] for col in features}
        # print(result_dict)

        for seed_i in list(range(10)):
            random.seed(seed_i)
            sample_size = len(self.data)
            data_subset = self.data.sample(n=sample_size, replace=True, random_state=seed_i)
            num_features = round(len(features)*0.6)
            sub_features = random.sample(features, num_features)

            if self.target_type in ['categorical', 'binary']: target = data_subset[self.target].astype('category')
            else: target = data_subset[self.target]

            dt.fit(data_subset[sub_features], target)

            result = permutation_importance(dt, data_subset[sub_features], target, n_repeats=10, random_state=seed_i, n_jobs=-1)
            
            for i, col in enumerate(sub_features):
                result_dict[col].append(result.importances_mean[i])

        results = [np.mean(result_dict[col]) if len(result_dict[col])>0 else 0 for col in features]

        self.dt_feature_importance = pd.DataFrame({'Feature': features, 'Importance': results}).sort_values(by='Importance', ascending=False)

        return self

    def _poly_feature_selection(self, feature_limit = 25):
        from sklearn.linear_model import Lasso, LogisticRegression
        from sklearn.preprocessing import PolynomialFeatures
        from sklearn.preprocessing import StandardScaler
        # create polynomials and interaction terms and scale data
        poly = PolynomialFeatures(degree=2, include_bias=True)
        scaler = StandardScaler()
        x_poly = poly.fit_transform(self.data[self.features])
        x = scaler.fit_transform(x_poly)
        

        # select appriate model for classification or regression
        if self.target_type in ['categorical', 'binary']:
            regularization = 1
            regularization_change = 0.2
            reg_param = 'C'
            model = LogisticRegression(random_state=0, penalty='l1', solver='liblinear', C=regularization)
            target = self.data[self.target].astype('category')
        else: 
            regularization = 0.1
            regularization_change = 5
            reg_param = 'alpha'
            model = Lasso(random_state=0, alpha=regularization)
            target = self.data[self.target]

        lr = model.fit(x, target)
        number_non_zero_coef = len([coef for coef in lr.coef_[0] if coef>0])

        while number_non_zero_coef > feature_limit:
            regularization = regularization * regularization_change
            model.set_params(**{reg_param: regularization})

            lr = model.fit(x, target)
            number_non_zero_coef = len([coef for coef in lr.coef_[0] if coef>0])
        
        poly_df = pd.DataFrame({'Feature': poly.get_feature_names_out(self.features), 'Importance': lr.coef_[0]})
        poly_df = poly_df[~poly_df['Feature'].isin(self.features)].sort_values(by='Importance', ascending=False)
        self.poly_features = poly_df[poly_df['Importance']>0]
        self.poly_features_list = poly_df['Feature'].to_list()


        temp = pd.DataFrame(x_poly, columns=poly.get_feature_names_out(self.features))
        temp = temp[self.poly_features['Feature'].to_list()].fillna(0)

        # temp = self.data[temp.columns]
        self.data[temp.columns] = temp
        self.features.extend(temp.columns)

        return self
    
    def _svd_filter(self):
        from sklearn.preprocessing import StandardScaler
        from sklearn.decomposition import TruncatedSVD
        from sklearn.cross_decomposition import PLSRegression

        scaler = StandardScaler()
        x = scaler.fit_transform(self.data[self.features])
        target = self.data[self.target]

        svd = TruncatedSVD(n_components=len(self.features))
        svd.fit(x)
        cum_var = np.cumsum(svd.explained_variance_ratio_)
        k = np.argmax(cum_var >= 0.90) + 1

        svd = TruncatedSVD(n_components=k)
        svd.fit(x)
        svd_features = ['svd_' + str(k) for k in range(k)]

        component_var = np.var(svd.transform(x),axis=0)
        
        # calcualte weighted SVD feature weights
        svd_data = (svd.components_)**2
        svd_weights = np.sum(svd_data * component_var.reshape(-1,1), axis=0)


        # scale svd_weights using VIP
        x = pd.DataFrame(self.data[self.features])
        pls = PLSRegression(n_components=2)
        pls.fit(x,target)

        def calculate_vip(pls_model, X):
            t = pls_model.x_scores_
            w = pls_model.x_weights_
            q = pls_model.y_loadings_
            
            p, h = w.shape  # p = number of features, h = number of components
            
            # Sum of squares explained by each component for Y
            ssq = np.sum(t**2, axis=0) * np.sum(q**2, axis=0)
            
            vip = np.zeros((p,))
            total_ssq = np.sum(ssq)
            
            for i in range(p):
                weight = np.array([(w[i, j]**2) * ssq[j] for j in range(h)])
                vip[i] = np.sqrt(X.shape[1] * np.sum(weight) / total_ssq)
            
            return vip
        
        vip_scores = calculate_vip(pls, x)

        # Combine feature names and VIP scores
        vip_df = pd.DataFrame({
            'Feature': x.columns,
            'VIP_Score': vip_scores
        }).sort_values(by='VIP_Score', ascending=False)


        vip_df['Importance'] = svd_weights * vip_df['VIP_Score']

        self.svd_filter_df =  vip_df[vip_df['Importance']>1][['Feature', 'Importance']].sort_values(by='Importance', ascending=False)

        return self
