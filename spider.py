import sys,os

try:
    from osgeo import ogr
except: 
    import ogr

def spider(file, options):
    ds = ogr.Open(file)
    if ds is None:
        print 'Could not open ' + file
        sys.exit(1) #exit with an error code

    # get the driver for the output data
    driver = ds.GetDriver()

    facilitiesLayer = ds.GetLayerByName("AS_Facilities")
    feature_defn = facilitiesLayer.GetLayerDefn()
    costMatrixLayer = ds.GetLayerByName("AS_ODCostMatrix")
    costMatrix_defn = facilitiesLayer.GetLayerDefn()

    # loop through the input features
    for facility in facilitiesLayer:
        field_index = facility.GetFieldIndex("USERCODE")
        usercode = facility.GetField(field_index)
        print("Generating spider for USERCODE %s..." % usercode)

        if os.path.exists(usercode):
            if options.overwrite:
                os.remove(usercode)
        else:
            print("%s already exists.  Re-run with --overwrite if you wish."
                   % usercode)
            continue 

        # create the output file
        outDS = driver.CreateDataSource(usercode)
        if outDS is None:
            print 'Could not create file'
            sys.exit(1)
        outLayer = outDS.CreateLayer("spider",
                           geom_type = feature_defn.GetGeomType(),
                                 srs = facilitiesLayer.GetSpatialRef())

        # use the input FieldDefn to add fields to the output
        for i in range(costMatrix_defn.GetFieldCount()): 
            src_fd = costMatrix_defn.GetFieldDefn(i) 
            fd = ogr.FieldDefn( src_fd.GetName(), src_fd.GetType() ) 
            fd.SetWidth( src_fd.GetWidth() ) 
            fd.SetPrecision( src_fd.GetPrecision() ) 
            outLayer.CreateField( fd )

        # get the features where the End_USERCODE and the Start_AS_Usercode
        # match the USERCODE.
        sql_layer = ds.ExecuteSQL('SELECT * FROM AS_ODCostMatrix WHERE End_USERCODE = "%s" AND Start_AS_Usercode = "%s"' % (usercode, usercode))
        print("    %s features match USERCODE %s" % (sql_layer.GetFeatureCount(),usercode))

        # loop through the features and copy them.
        for feature in sql_layer:
            target_feature = ogr.Feature(feature_defn)
            target_feature.SetFrom(feature)
            target_feature.SetGeometry(feature.GetGeometryRef())
            # populate all the fields for this feature
            for i in range(feature.GetFieldCount()): 
                src_field = feature.GetField(i) 
                target_feature.SetField(i, src_field) 
            outLayer.CreateFeature(target_feature)
            target_feature.Destroy()
            feature.Destroy()

        # clean up
        ds.ReleaseResultSet( sql_layer )
        facility.Destroy()
        outDS.Destroy()

    ds.Destroy()

def main():
    """ Runs program and handles command line options """
    import optparse
    p = optparse.OptionParser(description='Creates spiders based on usercodes',
                     prog='spider',
                  version='spider 0.1',
                    usage='%prog filename')
    p.add_option("--overwrite", action="store_true", dest="overwrite", default=False)
    options, arguments = p.parse_args()
    if len(arguments) == 1:
        spider(file=arguments[0], options=options)
    else:
        p.print_help()

if __name__ == "__main__":
    main()
