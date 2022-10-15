import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import platform
import shap
import os

if platform.system() == "Darwin":
    plt.rc('font', family='AppleGothic')
elif platform.system() == "Windows":
    font_path = "C:/Windows/Fonts/NGULIM.TTF"
    font = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font)


def model_training(filename):
    output_dir = "../Output/Result/xgb"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    df = pd.read_csv(filename)

    y = df["누적단위면적당생산량"]

    exclude_list = []
    for col_name in df.columns:
        for field in ["농가", "품종", "색상", "면적", "온실종류", "온실수확박스수", "온실총생산량",  "정식일자", "첫생산일기준주차", "정식기준주차", "date", "year", "month", "day"]:
            if col_name.startswith(field):
                exclude_list.append(col_name)

    for e in exclude_list:
        del df[e]

    X = df.drop(["누적단위면적당생산량"], axis=1).select_dtypes(exclude=['object'])

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.6, random_state=777)

    if "Orange" in filename:
        cul = "주황색계"
        cor = "coral"
    elif "Red" in filename:
        cul = "적색계"
        cor = "red"
    else:
        cul = "황색계"
        cor = "gold"

    model = XGBRegressor()

    # model fitting
    model.fit(X_train, y_train)

    # model predict
    prediction = model.predict(X_test)

    mae = mean_absolute_error(prediction, y_test)
    r2 = r2_score(prediction, y_test)

#     plt.figure(figsize=(6, 6))
#     plt.scatter(prediction, y_test, alpha=0.6, color=cor)
#
#     if max(prediction) >= max(y_test):
#         plt.plot([0, max(prediction)], [0, max(prediction)], color="black", linestyle="--")
#     else:
#         plt.plot([0, max(y_test)], [0, max(y_test)], color="black", linestyle="--")
#
#     size = 18
#     params = {
#         'axes.labelsize': size * 1.5,
#         'axes.titlesize': size * 1.2,
#     }
#     plt.rcParams.update(params)
#
#     plt.title(cul)
#     plt.xlabel("Predict Value", fontsize=15)
#     plt.ylabel("Real Value", fontsize=15)
#     plt.tight_layout()
#     plt.savefig(os.path.join(output_dir, f"{cul}.png"), dpi=600)

    # shap
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)
    shap.summary_plot(shap_values, X_test, show=False)
    plt.savefig(os.path.join(output_dir, f"{cul}_shap.png"), dpi=600)

    return "R2: {:.2f} , MAE: {:.2f}".format(r2, mae)


def main():
    filename = [
        f"../Output/Data/FinalData/Week15/paprika(Orange).csv",
        f"../Output/Data/FinalData/Week15/paprika(Red).csv",
        f"../Output/Data/FinalData/Week16/paprika(Yellow).csv"
    ]

    for f in filename:
        data = model_training(f)
        print(data)


if __name__ == "__main__":
    main()