export interface CourseModel {
  VendorID: number;
  tpep_pickup_datetime: string;
  tpep_dropoff_datetime: string;
  passenger_count: number | null;
  trip_distance: number;
  RatecodeID: number | null;
  store_and_fwd_flag: number | null;
  PULocationID: number;
  DOLocationID: number;
  payment_type: number;
  fare_amount: number;
  extra: number;
  mta_tax: number;
  tip_amount: number;
  tolls_amount: number;
  improvement_surcharge: number;
  total_amount: number;
  congestion_surcharge: number;
  airport_fee: number;
  cbd_congestion_fee: number;
  trip_duration_min: number;
  pickup_hour: number;
  pickup_weekday: number;
}

export interface CoursesResponse {
  courses: CourseModel[];
  limit: number;
  offset: number;
}
