import {Injectable} from '@angular/core';
import {HttpErrorResponse, HttpEvent, HttpHandler, HttpInterceptor, HttpRequest} from '@angular/common/http';
import {catchError, EMPTY, Observable} from 'rxjs';
import {environment} from '../../environments/environment';
import {HANDLE_ERROR} from './context';
import {MatSnackBar} from '@angular/material/snack-bar';

@Injectable()
export class BackendInterceptor implements HttpInterceptor {

  constructor(private snackBar: MatSnackBar) {}

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    if (!request.url.startsWith('http')) {
      request = request.clone({
        url: `${environment.backendUrl}/${request.url}`
      });
    }
    const handleError = request.context.get(HANDLE_ERROR);
    if (handleError) {
      return next.handle(request).pipe(
        catchError((err: HttpErrorResponse) => {
          let message = `Terjadi kesalahan: ${err.message}`;
          console.error(message, err.error);
          this.snackBar.open(message);
          return EMPTY;
        }),
      );
    } else {
      return next.handle(request);
    }
  }
}
