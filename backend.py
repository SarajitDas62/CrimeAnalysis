"""
BACKEND.PY - Data Processing & Machine Learning Models
Handles all data operations and ML algorithms
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import warnings
warnings.filterwarnings('ignore')


class CrimeDataProcessor:
    """Process and clean crime data"""

    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = None

    def load_data(self, sample=False, n_rows=None):
        """Load CSV file"""
        if sample and n_rows:
            self.df = pd.read_csv(self.csv_path, nrows=n_rows)
        else:
            self.df = pd.read_csv(self.csv_path)
        return self.df

    def clean_data(self):
        """Clean dataset"""
        # Remove complete duplicates
        self.df = self.df.drop_duplicates()

        # Standardize column names (remove spaces, lowercase)
        self.df.columns = [col.strip().replace(' ', '_').lower() for col in self.df.columns]

        # Handle missing values with correct column names
        if 'vict_sex' in self.df.columns:
            self.df['vict_sex'].fillna('Unknown', inplace=True)
        if 'vict_descent' in self.df.columns:
            self.df['vict_descent'].fillna('Unknown', inplace=True)
        if 'weapon_used_cd' in self.df.columns:
            self.df['weapon_used_cd'].fillna(-1, inplace=True)
        if 'weapon_desc' in self.df.columns:
            self.df['weapon_desc'].fillna('Unknown Weapon', inplace=True)
        if 'premis_desc' in self.df.columns:
            self.df['premis_desc'].fillna('Unknown', inplace=True)

        # Remove rows with missing critical location data
        self.df = self.df.dropna(subset=['lat', 'lon'])

        return self.df

    def extract_features(self):
        """Extract useful features"""
        # Convert date columns to datetime
        self.df['date_occ'] = pd.to_datetime(self.df['date_occ'], errors='coerce')
        self.df['date_rptd'] = pd.to_datetime(self.df['date_rptd'], errors='coerce')

        # Extract time features
        self.df['hour'] = (self.df['time_occ'] // 100).astype(int)
        self.df['day_of_week'] = self.df['date_occ'].dt.day_name()
        self.df['month'] = self.df['date_occ'].dt.month
        self.df['year'] = self.df['date_occ'].dt.year
        self.df['date'] = self.df['date_occ'].dt.date

        # Standardize crime type names
        self.df['crm_cd_desc'] = self.df['crm_cd_desc'].str.strip().str.upper()

        return self.df

    def get_processed_data(self):
        """Get full processing pipeline"""
        self.load_data()
        self.clean_data()
        self.extract_features()
        return self.df


class HotspotDetector:
    """Detect crime hotspots using KMeans clustering"""

    def __init__(self, n_clusters=8):
        self.n_clusters = n_clusters
        self.model = None
        self.scaler = StandardScaler()
        self.centers = None

    def detect_hotspots(self, df):
        """Detect hotspots from lat/lon coordinates"""
        coords = df[['lat', 'lon']].values
        coords_scaled = self.scaler.fit_transform(coords)

        self.model = KMeans(n_clusters=self.n_clusters, random_state=42, n_init=10)
        clusters = self.model.fit_predict(coords_scaled)

        self.centers = self.scaler.inverse_transform(self.model.cluster_centers_)

        return clusters, self.centers


class CrimeRiskPredictor:
    """Predict crime risk based on hour, location, and type"""

    def __init__(self):
        self.model = None
        self.feature_encoders = {}
        self.feature_columns = None

    def prepare_features(self, df):
        """Encode categorical features"""
        features_df = df[['hour', 'area_name', 'crm_cd_desc', 'lat', 'lon']].copy()

        for col in ['area_name', 'crm_cd_desc']:
            le = LabelEncoder()
            features_df[col] = le.fit_transform(features_df[col].astype(str))
            self.feature_encoders[col] = le

        return features_df

    def train(self, df, target_col='crm_cd_desc'):
        """Train model to predict crime type"""
        X = df[['hour', 'area_name', 'lat', 'lon']].copy()

        le_area = LabelEncoder()
        X['area_name'] = le_area.fit_transform(X['area_name'].astype(str))
        self.feature_encoders['area_name'] = le_area

        le_crime = LabelEncoder()
        y = le_crime.fit_transform(df[target_col].astype(str))
        self.feature_encoders['crm_cd_desc'] = le_crime

        self.model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1, max_depth=15)
        self.model.fit(X, y)
        self.feature_columns = X.columns

        return self.model

    def predict_crime_type(self, hour, area_name, lat, lon):
        """Predict crime type for given inputs"""
        if self.model is None:
            return None

        le_area = self.feature_encoders.get('area_name')
        try:
            area_encoded = le_area.transform([area_name])[0]
        except:
            area_encoded = 0

        X_input = np.array([[hour, area_encoded, lat, lon]])
        prediction = self.model.predict(X_input)[0]

        le_crime = self.feature_encoders.get('crm_cd_desc')
        crime_type = le_crime.inverse_transform([prediction])[0]

        return crime_type

    def get_feature_importance(self):
        """Get feature importance from model"""
        if self.model is None:
            return None

        importances = self.model.feature_importances_
        features = self.feature_columns

        return dict(zip(features, importances))
