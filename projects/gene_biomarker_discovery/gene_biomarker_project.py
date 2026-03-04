"""
=================================================================
 GENE BIOMARKER DISCOVERY — YOUR CHALLENGE
 
 Story:
   Ek hospital ne 150 patients ka RNA sequencing kiya.
   200 genes ka expression measure hua har patient ke liye.
   Target: Disease severity score (higher = worse)
   
   BUT — sabse bada problem:
   Sirf kuch genes actually disease se related hain.
   Baaki sab noise hain (irrelevant genes).
   
   TERA KAM:
   1. Sahi model use karke disease predict kar
   2. Identify kar ki kaun se genes ACTUALLY matter karte hain
   3. Doctor ko report de (less genes = more actionable)
=================================================================
"""

from sklearn.pipeline import Pipeline
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, LassoCV, Ridge,ElasticNet
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)

# ═══════════════════════════════════════
# DATA — DON'T CHANGE THIS BLOCK
# ═══════════════════════════════════════
X, y, true_coef = make_regression(
    n_samples   = 150,
    n_features  = 200,
    n_informative = 15,
    noise       = 30,
    coef        = True,
    random_state = 42
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

true_causal_genes = np.where(true_coef != 0)[0]  # Cheating — only to verify at end!
print(f"Dataset ready: {X_train.shape[0]} train, {X_test.shape[0]} test patients")
print(f"Features: {X.shape[1]} genes | Target range: {y.min():.0f} to {y.max():.0f}")
print(f"(There are {len(true_causal_genes)} true causal genes — find them!)\n")

# ═══════════════════════════════════════
# TASK 1: Baseline — Plain Linear Regression
# ═══════════════════════════════════════
# Build a Pipeline: StandardScaler + LinearRegression
# Print Train R2 and Test R2
# Kya observe hota hai? Kyun?

# YOUR CODE HERE:
ols=LinearRegression()
ols.fit(X_train,y_train)

predicted=ols.predict(X_test)
print(f"r2train {ols.score(X_train,y_train)} r2 test {ols.score(X_test,y_test)}")
''' r2train 1.0 r2 test 0.5866115206952053 
overfit hai bhai '''
# ═══════════════════════════════════════
# TASK 2: The Real Fix — Lasso Regression
# ═══════════════════════════════════════
# Use LassoCV (auto finds best alpha) inside a Pipeline
# Print:
#   - Best alpha found
#   - How many genes are NON-ZERO (selected)
#   - How many genes are ZERO (eliminated)
#   - Train R2 and Test R2
# 
# Hint: lasso_pipe.named_steps['lasso'].coef_ gives coefficients
#       np.where(coef != 0)[0] gives indices of nonzero features

# YOUR CODE HERE:
lasso_pipe=Pipeline([
    ('scaler',StandardScaler()),
    ('lasso',LassoCV(cv=5))
])
lasso_pipe.fit(X_train,y_train)
coef=lasso_pipe.named_steps['lasso'].coef_


# ═══════════════════════════════════════
# TASK 3: Verify — Did Lasso find the right genes?
# ═══════════════════════════════════════
# genes_selected = indices where Lasso coef != 0
# true_causal_genes = the actual causal genes (given above)
# 
# Calculate:
#   - How many true causal genes did Lasso correctly find?
#   - How many false positives (noise genes Lasso included)?
#   - How many true genes did Lasso miss?

# YOUR CODE HERE:

non_zero=np.where(coef != 0)[0]

correctly_found = np.intersect1d(non_zero, true_causal_genes)
false_positives = np.setdiff1d(non_zero, true_causal_genes)
missed_genes = np.setdiff1d(true_causal_genes, non_zero)

print(f"Correctly identified: {len(correctly_found)} / {len(true_causal_genes)}")
print(f"False Positives (Noise included): {len(false_positives)}")
print(f"Missed Genes: {len(missed_genes)}")


# print(coef)
print(f"non zero coef {len(non_zero)}")
print(f"zero coef {len(coef)-len(non_zero)}")
print(f"r2train {lasso_pipe.score(X_train,y_train)} r2 test {lasso_pipe.score(X_test,y_test)}")

# ═══════════════════════════════════════
# TASK 4: Ridge Comparison
# ═══════════════════════════════════════
# Try Ridge with alphas = [0.1, 1, 10, 100, 1000]
# For each alpha:
#   - Fit Pipeline(StandardScaler + Ridge)
#   - Print Test R2
#   - Print how many genes have |coef| > 0.01 (near non-zero)
# 
# Question to answer in a comment: 
#   Ridge vs Lasso — which is better for gene selection? Why?

# YOUR CODE HERE:

alphas=[0.1,1,10,100,1000]
for i in alphas:

    pipe=Pipeline([
        ('scalar',StandardScaler()),
        ('ridge',Ridge(alpha=i))
    ])
    pipe.fit(X_train,y_train)
    print(pipe.score(X_test,y_test))
    print(np.where(np.abs(pipe.named_steps['ridge'].coef_) >0.1))
    # obiviously lasso is better than ridge where no. of features are more than samnple or nearly more than needed 


# print(gds.results_cv_results_)
# ═══════════════════════════════════════
# TASK 5: ElasticNet with GridSearch
# ═══════════════════════════════════════
# Build Pipeline with ElasticNet
# GridSearch over:
# cv=5, scoring='r2'
# 
# Print best params and best test R2
# How many genes did ElasticNet select?
# FIX: Grid expanded — LassoCV searches 100+ alphas, our grid was too small!
# Rule: GridSearch can only be as good as the grid you give it!
alphagd = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10]  # wider range!
l1_ratio = [0.2, 0.5, 0.7, 0.9, 0.95, 1.0]                 # 1.0 = pure Lasso!

# YOUR CODE HERE:
paramgd = {
    'elasticnet__alpha':    alphagd,
    'elasticnet__l1_ratio': l1_ratio
}
pipegd = Pipeline([
    ('scaler', StandardScaler()),
    ('elasticnet', ElasticNet(max_iter=10000))
])
gds = GridSearchCV(pipegd, param_grid=paramgd, cv=5, scoring='r2')
gds.fit(X_train, y_train)

print(f"Best params: {gds.best_params_}")
n_selected = np.sum(gds.best_estimator_.named_steps['elasticnet'].coef_ != 0)
print(f"Genes selected: {n_selected}")

# FIX: Compare CV score vs TEST score (SAME metric, same scale!)
enet_test_r2  = r2_score(y_test, gds.best_estimator_.predict(X_test))
lasso_test_r2 = lasso_pipe.score(X_test, y_test)
print(f"ElasticNet CV R2:   {gds.best_score_:.3f}  (cross-val on train)")
print(f"ElasticNet Test R2: {enet_test_r2:.3f}   (held-out test)")
print(f"Lasso Test R2:      {lasso_test_r2:.3f}   (for fair comparison)")
print(f"Winner: {'ElasticNet' if enet_test_r2 > lasso_test_r2 else 'Lasso'}")
print("NOTE: best_score_ = CV score not test R2 — compare test vs test only!")

# ═══════════════════════════════════════
# TASK 6: Plot — Actual vs Predicted
# ═══════════════════════════════════════
# For your BEST model, make a scatter plot:
#   X-axis: Actual disease score (y_test)
#   Y-axis: Predicted disease score
#   + Add perfect prediction diagonal line (red dashed)
#   + Title should show model name and Test R2

# YOUR CODE HERE:
pred =lasso_pipe.predict(X_test )# gds.best_estimator_.predict(X_test)  # Best model predictions

# FIX: scatter plot with CORRECT axes
# Rule: X-axis = Actual (what really happened)
#       Y-axis = Predicted (what model said)
#       Perfect model = all points ON the diagonal line
plt.figure(figsize=(7, 6))
plt.scatter(y_test, pred, alpha=0.7, edgecolors='k', linewidth=0.5, color='steelblue')

# FIX: Diagonal line needs TWO POINTS: [x_start, x_end], [y_start, y_end]
# plt.plot(single_number) → ERROR/wrong (no line!)
lo = min(y_test.min(), pred.min())
hi = max(y_test.max(), pred.max())
plt.plot([lo, hi], [lo, hi], 'r--', linewidth=2, label='Perfect prediction')

plt.xlabel('Actual Disease Score')
plt.ylabel('Predicted Disease Score')
plt.title(f'ElasticNet: Actual vs Predicted\nTest R2 = {r2_score(y_test, pred):.3f}')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
# plt.savefig('g:/plans/mml/ml_learning_plan/statistics_lessons/code/revision/gene_plot.png', dpi=100)
plt.show()
print("Plot saved as gene_plot.png")

# ═══════════════════════════════════════
# TASK 7 (BONUS): Biomarker Report
# ═══════════════════════════════════════
# From Lasso model, create a ranked list of top 10 genes:
#   Gene name (just "Gene_XXX"), coefficient magnitude (importance)
#   Print in table format
# 
# This is what you'd actually send to a biology lab!

# make_regression has no feature names — sirf numbers hain
# Solution: khud gene names banao (Gene_000 to Gene_199)
gene_names = [f"Gene_{i:03d}" for i in range(X.shape[1])]

# Lasso ke non-zero genes ki list (index + name + importance)
non_zero_ids = np.where(coef != 0)[0]
gene_importance = [
    (gene_names[i], abs(coef[i]), i in true_causal_genes)
    for i in non_zero_ids
]
# Sort by importance (highest first)
gene_importance_sorted = sorted(gene_importance, key=lambda x: -x[1])

print(f"\n{'Rank':<6} {'Gene':<12} {'Importance':>12}  {'Real Cause?'}")
print("-" * 48)
for rank, (gene, imp, is_real) in enumerate(gene_importance_sorted[:10], 1):
    bar = "=" * int(imp / gene_importance_sorted[0][1] * 15)
    verdict = "YES" if is_real else "False positive"
    print(f"{rank:<6} {gene:<12} {imp:>12.2f}  {verdict}  {bar}")

print("\nDone! Compare your answers with gene_biomarker_project.py")
