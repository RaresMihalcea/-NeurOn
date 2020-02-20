import { Component, OnInit, Input } from '@angular/core';

import * as dracula from 'graphdracula';
import { IfStmt } from '@angular/compiler';

@Component({
	selector: 'app-graph',
	templateUrl: './graph.component.html',
	styleUrls: ['./graph.component.scss']
})
export class GraphComponent implements OnInit {

	// @Input()
	// matrix;

	constructor() { 
	}

	visualise(matrix: number[][], somaIndex: number): void {
		this.removeOld();
		var Graph = dracula.Graph
		var Renderer = dracula.Renderer.Raphael
		var Layout = dracula.Layout.Spring
	
		var graph = new Graph()
		for(var i = 0; i < matrix.length; i++) {
			for(var j = matrix[i].length - 1; j > i; j--) {
				console.log(j);
				
				if(i == somaIndex && matrix[i][j] !== 0) {
					
					graph.addEdge('Soma', j, { directed: false, label: matrix[i][j]});
				}
				else if(matrix[i][j] !== 0) {
					graph.addEdge(i, j, { directed: false, label: matrix[i][j]});
				}
			}
		}
	
		var layout = new Layout(graph);
		var renderer = new Renderer('#paper', graph, 300, 300);
		renderer.draw();
	}

	removeOld(): void {
		var elem = document.querySelector('#paper');
		elem.parentNode.removeChild(elem);
		var elem = document.querySelector('#paper-container');
		var newDiv = document.createElement('div');
		newDiv.setAttribute('id', 'paper');
		newDiv.style.border = "1px solid black";
		elem.appendChild(newDiv);
	}

	ngOnInit(): void {
		var Graph = dracula.Graph
		var Renderer = dracula.Renderer.Raphael
		var Layout = dracula.Layout.Spring
	
		var graph = new Graph()
	
		graph.addEdge('Soma', '1', { directed: false, label: 50});
	
		var layout = new Layout(graph)
		var renderer = new Renderer('#paper', graph, 300, 300)
		renderer.draw()
	}

}
