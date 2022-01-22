import {Component, forwardRef, Input} from '@angular/core';
import {HttpClient, HttpEvent, HttpEventType, HttpHeaders, HttpRequest} from '@angular/common/http';
import {finalize, last, tap} from 'rxjs';
import {MatSnackBar} from '@angular/material/snack-bar';
import {animate, style, transition, trigger} from '@angular/animations';
import {ControlValueAccessor, NG_VALUE_ACCESSOR} from '@angular/forms';
import {environment} from '../../../environments/environment';
import {OidcSecurityService} from 'angular-auth-oidc-client';

@Component({
  selector: 'app-image-upload',
  templateUrl: './image-upload.component.html',
  styleUrls: ['./image-upload.component.css'],
  animations: [
    trigger('show', [
      transition(':enter', [
        style({opacity:0, position: 'absolute'}),
        animate('250ms', style({opacity: 1})),
      ]),
      transition(':leave', [
        style({opacity:1, position: 'absolute'}),
        animate('350ms', style({opacity: 0})),
      ]),
    ]),
  ],
  providers: [
    {provide: NG_VALUE_ACCESSOR, multi: true, useExisting: forwardRef(() => ImageUploadComponent)},
  ],
})
export class ImageUploadComponent implements ControlValueAccessor {

  @Input() fileServerUrl = environment.fileServerUrl;
  @Input() bucket: string|null = '';

  private _uploadedFilename: string|null = null;
  uploadProgress = 0;
  focus = false;
  onChange = (_: string|null) => {};
  onTouched = () => {};

  constructor(private httpClient: HttpClient, private snackBar: MatSnackBar, private oidcSecurityService: OidcSecurityService) { }

  get uploadedFilename(): string|null {
    return this._uploadedFilename;
  }

  set uploadedFilename(value: string|null) {
    this._uploadedFilename = value;
    this.onChange(value);
  }

  onFileSelected(fileElement: HTMLInputElement) {
    if ((fileElement.files == null) || (fileElement.files.length === 0)) {
      this.uploadedFilename = null;
      return;
    }
    const formData = new FormData();
    const file = fileElement.files[0];
    formData.append('file', file);
    const req = new HttpRequest('POST', `${this.fileServerUrl}${this.bucket ? '/' + this.bucket : ''}/upload`, formData, {
        reportProgress: true, responseType: 'json',
        headers: new HttpHeaders().append('Authorization', `Bearer ${this.oidcSecurityService.getAccessToken()}`)
    });
    this.httpClient.request(req).pipe(
      tap((event: HttpEvent<any>) => this.handleUploadEvent(event, file)),
      finalize(() => this.uploadProgress = 0),
      last(),
    ).subscribe((result) => {
      if (result.type === HttpEventType.Response) {
        if (!result.ok) {
          this.snackBar.open('Maaf, terjadi kesalahan saat meng-upload file');
          return;
        }
        const responseBody = result.body as {filename: string};
        this.uploadedFilename = responseBody.filename;
      }
    });
    this.onTouched();
  }

  handleUploadEvent(event: HttpEvent<any>, file: File) {
    switch (event.type) {
      case HttpEventType.Sent:
        console.log(`Uploading file ${file.name} of size ${file.size}.`);
        break;
      case HttpEventType.UploadProgress:
        this.uploadProgress = Math.round((event.loaded / (event.total ?? 0)) * 100);
        break;
    }
  }

  delete() {
    this.uploadedFilename = null;
  }

  writeValue(value: string): void {
    this._uploadedFilename = value ?? null;
  }

  registerOnChange(fn: (_: string|null) => void): void {
    this.onChange = fn;
  }

  registerOnTouched(fn: () => void): void {
    this.onTouched = fn;
  }

}
