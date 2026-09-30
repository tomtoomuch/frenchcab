import { Component, OnInit } from '@angular/core';
import { Course } from '../models/course.model';
import { CourseService } from '../course-service';

@Component({
  imports: [],
  selector: 'app-course',
  styleUrl: './course.scss',
  templateUrl: './course.html',
})
export class CoursesComponent implements OnInit {

  courses: Course[] = [];

  currentPage = 1;
  pageSize = 10;
  totalCourses = 0;

  selectedCourse: Course | null = null;

  constructor(private courseService: CourseService) {}

  ngOnInit(): void {
    this.loadCourses();
  }

  loadCourses(): void {
    this.courseService
      .getCourses(this.currentPage, this.pageSize)
      .subscribe({
        next: (response) => {
          this.courses = response.data;
          this.totalCourses = response.total;
        },
        error: (error) => {
          console.error('Erreur lors du chargement des courses', error);
        }
      });
  }

  nextPage(): void {
  if (this.currentPage < this.totalPages()) {
    this.currentPage++;
    this.loadCourses();
  }
}

  previousPage(): void {
    if (this.currentPage > 1) {
      this.currentPage--;
      this.loadCourses();
    }
  }

  totalPages(): number {
    return Math.ceil(this.totalCourses / this.pageSize);
  }

  showDetails(course: Course): void {
    this.selectedCourse = course;
  }

  closeDetails(): void {
    this.selectedCourse = null;
  }
}
