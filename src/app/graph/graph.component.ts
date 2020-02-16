import { Component, OnInit } from '@angular/core';

import * as dracula from 'graphdracula';

@Component({
	selector: 'app-graph',
	templateUrl: './graph.component.html',
	styleUrls: ['./graph.component.scss']
})
export class GraphComponent implements OnInit {

	constructor() { 
		this.drawGraph()
	}

	ngOnInit(): void {
		var Graph = dracula.Graph
		var Renderer = dracula.Renderer.Raphael
		var Layout = dracula.Layout.Spring
	
		var graph = new Graph()
	
		graph.addEdge('Soma', '1', { directed: false, label: 50});
	// 	 graph.addEdge('Script1', 'Loop', {
	// 	stroke: '#bfa' , fill: '#56f', label: 'Meat-to-Apple', directed: true
	//   });
		// graph.addEdge('Apple', 'Kiwi')
		// graph.addEdge('Apple', 'Dragonfruit')
		// graph.addEdge('Dragonfruit', 'Banana')
		// graph.addEdge('Kiwi', 'Banana')
	
		var layout = new Layout(graph)
		var renderer = new Renderer('#paper', graph, 300, 300)
		renderer.draw()
	}

	drawGraph(): void {
	}

}
