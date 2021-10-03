import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CancionJoinUserComponent } from './cancion-join-user.component';

describe('CancionJoinUserComponent', () => {
  let component: CancionJoinUserComponent;
  let fixture: ComponentFixture<CancionJoinUserComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CancionJoinUserComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CancionJoinUserComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
