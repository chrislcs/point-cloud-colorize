{
	"pipeline":[
		{"type": "readers.las",
		"filename":"/var/data/arnot/c_10cn2_color.laz",
		"spatialreference":"EPSG:28992"},
	{"type":"filters.python",
	"script":"normalize.py",
	"function":"normalize"},
	{"type":"writers.las",
	"filename":"/var/data/arnot/AHN/filtered_laz.laz"}
]
}


