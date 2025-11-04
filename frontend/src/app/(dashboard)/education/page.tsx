'use client';

import { useEffect, useState } from 'react';
import { useAuthStore } from '@/store/auth-store';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Button } from '@/components/ui/button';
import { educationApi } from '@/lib/api/education';
import type { EducationProgress } from '@/types/education';
import { GraduationCap, BookOpen } from 'lucide-react';

export default function EducationPage() {
  const { user } = useAuthStore();
  const [courses, setCourses] = useState<EducationProgress[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (user?.id) {
      loadCourses();
    }
  }, [user]);

  const loadCourses = async () => {
    try {
      if (user?.id) {
        const coursesData = await educationApi.getProgress(user.id);
        setCourses(coursesData);
      }
    } catch (error) {
      console.error('Failed to load courses:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <div className="text-center py-8">Loading courses...</div>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Education</h1>
        <p className="text-muted-foreground">Learn about investing</p>
      </div>

      {courses.length === 0 ? (
        <Card>
          <CardContent className="py-12 text-center">
            <GraduationCap className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
            <h3 className="text-xl font-semibold mb-2">No Courses Yet</h3>
            <p className="text-muted-foreground">
              Educational courses will be available here soon.
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-6 md:grid-cols-2">
          {courses.map((course) => (
            <Card key={course.id} className="portfolio-card">
              <CardHeader>
                <div className="flex items-center gap-3">
                  <BookOpen className="h-8 w-8 text-primary" />
                  <div>
                    <CardTitle>{course.course_name}</CardTitle>
                    <CardDescription>Course ID: {course.course_id}</CardDescription>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span className="text-muted-foreground">Progress</span>
                      <span className="font-medium">{course.progress_percent}%</span>
                    </div>
                    <Progress value={course.progress_percent} className="h-2" />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground mb-2">Completed Modules</p>
                    <div className="flex flex-wrap gap-2">
                      {course.completed_modules.map((module, index) => (
                        <span
                          key={index}
                          className="text-xs px-2 py-1 bg-primary/10 text-primary rounded"
                        >
                          {module}
                        </span>
                      ))}
                    </div>
                  </div>
                  <Button variant="outline" className="w-full">
                    Continue Learning
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
