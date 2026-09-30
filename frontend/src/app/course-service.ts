

import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CourseModel } from './course/course.model';

interface CoursesResponse {
  data: CourseModel[];
  total: number;
}

@Injectable({
  providedIn: 'root'
})
export class CourseService {

  private apiUrl = 'http://localhost:3000/api/courses';

  constructor(private http: HttpClient) {}

  getCourses(page: number, limit: number): Observable<CoursesResponse> {

    const params = new HttpParams()
      .set('page', page)
      .set('limit', limit);

    return this.http.get<CoursesResponse>(
      this.apiUrl,
      { params }
    );
  }
}