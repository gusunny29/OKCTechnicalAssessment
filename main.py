import math
import string
import pandas as pd


def print_shots_by_zone(shot_region_df: pd.DataFrame):
    shot_attempts_by_region = shot_region_df.groupby('team')['region'].value_counts(normalize=True)
    print(f'Attempt Percentages: \n{shot_attempts_by_region.round(3)}')


def print_values(shot_region_df: pd.DataFrame):
    print_shots_by_zone(shot_region_df)


def classify_shot(shot_df: pd.DataFrame) -> pd.DataFrame:
    """
    Classifies each shot as one of 3 categories: 2PT, C3 or NC3
    :param shot_df: The dataframe containing shot information
    :return: a new dataframe containing three columns: team, fgmade and region
    """
    shot_region_df = shot_df.copy()
    for i, row in shot_region_df.iterrows():
        region = calculate_shot_region(row)
        shot_region_df.at[i, 'region'] = region

    # drop x and y in place since they're no longer needed
    shot_region_df.drop(['x', 'y'], axis=1, inplace=True)

    return shot_region_df


def calc_shots_made(shot_df: pd.DataFrame):
    shot_region_df = shot_df.copy()
    shot_dist_by_region = shot_region_df.groupby(["team", "region"])["fgmade"].value_counts(normalize=False)
    return shot_dist_by_region


def print_efg(efg_val: float, region: string):
    print(region + f": {efg_val:,.3f}")


def shot_efg(shots_made_by_region: pd.DataFrame):
    """
        Calculates the efg for each region for each team and prints out the correct efg
        :param shots_made_by_region: parsed dataframe representing the made and missed shots for a region
        """
    shots_dist = shots_made_by_region.copy()
    # A TEAM EFGS
    a2pt_efg = calc_efg(shots_dist[1], shots_dist[0] + shots_dist[1], 0)
    a3pc_efg = calc_efg(shots_dist[3], shots_dist[2] + shots_dist[3], shots_dist[3])
    a3pnc_efg = calc_efg(shots_dist[5], shots_dist[4] + shots_dist[5], shots_dist[5])
    # B TEAM EFGS
    b2pt_efg = calc_efg(shots_dist[7], shots_dist[6] + shots_dist[7], 0)
    b3pc_efg = calc_efg(shots_dist[9], shots_dist[8] + shots_dist[9], shots_dist[9])
    b3pnc_efg = calc_efg(shots_dist[11], shots_dist[10] + shots_dist[11], shots_dist[11])

    # Printing out EFG values
    print("\nEFG Values for Team A and B:")
    print_efg(a2pt_efg, "A2PT")
    print_efg(a3pc_efg, "A3PC")
    print_efg(a3pnc_efg, "A3PNC")
    print_efg(b2pt_efg, "B2PT")
    print_efg(b3pc_efg, "B3PC")
    print_efg(b3pnc_efg, "B3PNC")


def calculate_shot_region(row: pd.Series) -> str:
    """
    3PT Corner: y < 7.8 = and (x < -22.0 OR x > 22.0)
    3PT Non-Corner: pythagorean length > 23.75 while y > 7.8
    2PT: everything else
    """
    if row['y'] <= 7.8:
        if abs(row['x']) > 22.0:
            return '3PC'
    if calc_hypotenuse(row['x'], row['y']) > 23.75 and row['y'] > 7.8:
        return '3PNC'
    return '2PT'


def calc_hypotenuse(x: float, y: float) -> float:
    """
    Calculates hypotenuse distance with given coordinates
    :param x: distance from coordinate in x-direction
    :param y: distance from coordinate in y-direction
    :return: hypotenuse distance from coordinate
    """
    return math.sqrt(x * x + y * y)


def calc_efg(fgm: int, fga: int, threes_made: int):
    """
            Calculates hypotenuse distance with given coordinates
            :param fgm: field goals made in total in region
            :param fga: field goals attempted in region
            :param threes_made: number of 3s made in region
            :return: efg value for given area
            """
    return (fgm + 0.5 * threes_made) / fga


shot_df = pd.read_csv('Datasets/shots_data.csv')
shot_df.head()

# Classify each shot based on if it's a 3PC, 3PNC or 2PT
shot_region_df = classify_shot(shot_df)
shot_region_df.head()

# Print valid shot attempt distribution
print_values(shot_region_df)
shot_region_df.head()

# Calculate and print the efg for each region
shot_distribution_by_region = calc_shots_made(shot_region_df)
shot_efg(shot_distribution_by_region)
