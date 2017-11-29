from sklearn.ensemble import RandomForestRegressor


def get_forest_reg(data, labels):
  forest_reg = RandomForestRegressor(random_state=42)
  forest_reg.fit(data, labels)

  return forest_reg