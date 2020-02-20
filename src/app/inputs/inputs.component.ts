import { Component, OnInit, ViewChild } from '@angular/core';
import { GraphComponent } from '../graph/graph.component';

@Component({
	selector: 'app-inputs',
	templateUrl: './inputs.component.html',
	styleUrls: ['./inputs.component.scss']
})
export class InputsComponent implements OnInit {

	@ViewChild(GraphComponent, {static: false}) child;

	// Dendritic Params
	a: number = 2;
	C: number = 1;
	R: number = 2000;
	Ra: number = 100;
	L: number = 5;
	r: number = 1;
	
	// Somatic Params
	a_soma: number = 25; 
	C_soma: number = 1;
	R_soma: number = 2000;
	L_soma: number = 5;
	r_soma: number = 1;
	
	// Stimulus Params
	omega: number = 0.003; 
	A: number = 0.2;
	
	// Type of algo
	frequencyDomainFlag: number;
	
	// Geometry vars
	matrixInput: string = "0 50\n50 0";
	matrix: any = [];
	somaIndex: number = 0;
	
	// Error paras
	errors: boolean = false;
	varErrors = [];
	matrixErrors = new Set();
	
	constructor() { }
	
	ngOnInit(): void {}
	
	runAlgo(frequencyDomainFlag: number): void {
		this.checkInputs();
		if(!this.errors) {
			console.log('run');
			this.frequencyDomainFlag = frequencyDomainFlag;
			let data = this.buildData();
		}
	}

	buildData(): any {

	}

	buildMatrix(): number[][] {
		let matrix = [];
		let linesArr = this.matrixInput.split("\n");

		for(var i = 0; i < linesArr.length; i++) {
			let line = linesArr[i].split(" ");
			let numArray = [];
			for(var j = 0; j < line.length; j++) {
				let num = parseInt(line[j])
				if(num !== NaN)
					numArray.push(num);
			}
			matrix.push(numArray);
		}

		return matrix;
	}

	checkMatrix(): void {
		this.matrix = this.buildMatrix();
		
		for(var i = 0; i < this.matrix.length; i++) {
			for(var j = 0; j < this.matrix[i].length; j++) {
				
				if(this.matrix.length != this.matrix[i].length) {
					this.matrixErrors.add("Matrix is not square.");
					this.errors = true;
				}

				if(this.matrix[i][j] < 0) {
					this.matrixErrors.add("Found negative length in geometry matrix.");
					this.errors = true;
				}

				console.log(this.matrix[i][j], this.matrix[j][i]);
				console.log(this.matrixErrors);
				if(this.matrix[i][j] != this.matrix[j][i]) {
					console.log('GHEEEEEEEEEEE')
					this.matrixErrors.add("Matrix is not symmetric along the diagonal.");
					console.log(this.matrixErrors);
					this.errors = true;
				}

				if(i === j && this.matrix[i][j] !== 0) {
					this.matrixErrors.add("Matrix diagonal contains non-zero values.");
					this.errors = true;
				}
			}
		}

		if(this.somaIndex >= this.matrix.length || this.somaIndex < 0 || this.somaIndex % 1 != 0) {
			this.matrixErrors.add("Soma has an invalid index.");
			this.errors = true;
		}

		if(!this.errors) {
			let visitedNodes = this.bfs(this.matrix, this.somaIndex);
			if(visitedNodes !== this.matrix.length) {
				console.log(visitedNodes);
				this.matrixErrors.add("Graph is not connected.");
				this.errors = true; 
			}
		}
	}

	bfs(matrix: number[][], somaIndex): number {
		let queue = [somaIndex];
		let visited = new Set();

		while(queue.length !== 0) {
			let rowIndex = queue.shift();
			for(var i = 0; i < matrix[rowIndex].length; i++) {
				if(matrix[rowIndex][i] !== 0) {
					if(!visited.has(i)) {
						queue.push(i);
					}
					// if(queue.includes(i)) {
					// 	this.matrixErrors.add("Graph contains cycles.");
					// 	this.errors = true; 
					// }
				}
			}
			visited.add(rowIndex);
		}

		return visited.size;
	}

	visualiseMatrix(): void {
		this.matrixErrors = new Set();
		console.log(this.varErrors);
		if(this.varErrors.length === 0) {
			this.errors = false;
		}
		this.checkMatrix();
		this.child.visualise(this.matrix, this.somaIndex);
	}

	checkInputs(): void {
		this.varErrors = [];
		this.matrixErrors.clear();
		this.errors = false;
		this.checkMatrix();
		this.checkOneInput(this.a, "Diameter");
		this.checkOneInput(this.C, "Membrane Capacitance");
		this.checkOneInput(this.R, "Passive Unit Area Resistance");
		this.checkOneInput(this.Ra, "Specific Cytoplasmic Resistivity");
		this.checkOneInput(this.L, "Inductance");
		this.checkOneInput(this.r, "Series Resistance");
		this.checkOneInput(this.a_soma, "Somatic Diameter");
		this.checkOneInput(this.C_soma, "Somatic Membrane Capacitance");
		this.checkOneInput(this.R_soma, "Somatic Passive Unit Area Resistance");
		this.checkOneInput(this.L_soma, "Somatic Inductance");
		this.checkOneInput(this.r_soma, "Soma Series Resistance");
		this.checkOneInput(this.omega, "Stimulus");
		this.checkOneInput(this.A, "A");
	}

	checkOneInput(val, name): boolean {
		if(val < 0 || val === undefined || val == null) {
			this.varErrors.push(name);
			this.errors = true;
			return true;
		} 
		return false;
	}

}
