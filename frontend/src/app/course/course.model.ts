export interface CourseModel {
  id: string;
  version: string;
  created_at: string;
  updated_at: string;

  vendorid: string;
  tpep_pickup_datetime: string;
  tpep_dropoff_datetime: string;
  passenger_count: number;
  trip_distance: number;
  ratecodeid: string;
  store_and_fwd_flag: string;

  pulocationid: string;
  dolocationid: string;
  payment_type: string;

  fare_amount: number;
  extra: number;
  mta_tax: number;
  tip_amount: number;
  tolls_amount: number;
  improvement_surcharge: number;
  total_amount: number;
  congestion_surcharge: number;
  airport_fee: number;
}