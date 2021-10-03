import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CancionListComponent } from './cancion-list/cancion-list.component';
import { AppHeaderModule } from '../app-header/app-header.module';
import { CancionDetailComponent } from './cancion-detail/cancion-detail.component';
import { CancionCreateComponent } from './cancion-create/cancion-create.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { CancionEditComponent } from './cancion-edit/cancion-edit.component';
import { CancionJoinUserComponent } from './cancion-join-user/cancion-join-user.component';
import { CancionCommentComponent } from './cancion-comment/cancion-comment.component'


@NgModule({
  declarations: [CancionListComponent, CancionDetailComponent, CancionCreateComponent, CancionEditComponent,
    CancionCommentComponent,CancionJoinUserComponent],
  imports: [
    CommonModule, AppHeaderModule, FormsModule, ReactiveFormsModule
  ],
  exports:[CancionListComponent, CancionDetailComponent, CancionCreateComponent,
    CancionEditComponent, CancionCommentComponent]
})
export class CancionModule { }
