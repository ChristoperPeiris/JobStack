import { Component, OnInit } from '@angular/core';
import { Register } from '../shared/register';
import { User } from '../auth/user';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

  users : User;
  
}