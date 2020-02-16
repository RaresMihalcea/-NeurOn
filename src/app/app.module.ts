import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { IpcService } from './services/ipc.service';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { InputsComponent } from './inputs/inputs.component';
import { MatButtonModule } from '@angular/material/button'; 

@NgModule({
	declarations: [
		AppComponent,
		InputsComponent
	],
	imports: [
		BrowserModule,
		AppRoutingModule,
		BrowserAnimationsModule,
		MatFormFieldModule,
		MatInputModule,
		MatButtonModule
	],
	providers: [IpcService],
	bootstrap: [AppComponent]
})
export class AppModule { }
