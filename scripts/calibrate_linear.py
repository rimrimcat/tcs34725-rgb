import pandas as pd
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error, r2_score


if __name__ == "__main__":
    df = pd.read_csv("data/test.csv", header=None)
    df.columns = ["rt", "gt", "bt", "ct", "r", "g", "b"]
    df["rt2"] = (df["rt"])**2
    df["gt2"] = (df["gt"])**2
    df["bt2"] = (df["bt"])**2

    X = df[["rt", "gt", "bt", "rt2", "gt2", "bt2"]].to_numpy()
    Y = df[["r", "g", "b"]].to_numpy()
    

    func = Lasso(max_iter=10000,random_state=42).fit(X, Y)
    print(
        "COEFFS\n",
        str(func.coef_).replace("],", "],\n").replace("[", "{").replace("]", "}") + ";",
    )
    print(
        "INTERCEPTS\n", str(func.intercept_).replace("[", "{").replace("]", "}") + ";"
    )

    r2 = r2_score(Y, (func.coef_ @ (X).T).T + func.intercept_)
    mse = mean_squared_error(Y, (func.coef_ @ (X).T).T + func.intercept_)
    print("R2 Score:", r2)
    print("MSE:", mse)
