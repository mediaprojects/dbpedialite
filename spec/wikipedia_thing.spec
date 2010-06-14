require File.dirname(__FILE__) + "/spec_helper.rb"
require 'wikipedia_thing'

describe WikipediaThing do

  context "creating an article from a page id" do
    before :each do
      WikipediaApi.expects(:query).never
      @thing = WikipediaThing.for(52780)
    end

    it "should return an object of type WikipediaThing" do
      @thing.class.should == WikipediaThing
    end

    it "should have the correct URI" do
      @thing.uri.to_s.should == 'http://dbpedialite.org/things/52780#thing'
    end

    it "should not have co-ordinates" do
      @thing.should_not have_coordinates
    end
  end

  context "creating an thing from a page title" do
    before :each do
      WikipediaApi.expects(:query).once.returns({'52780'=>{'pageid'=>52780}})
      @thing = WikipediaThing.for_title('U2')
    end

    it "should return an object of type WikipediaThing" do
      @thing.class.should == WikipediaThing
    end

    it "should have the correct URI" do
      @thing.uri.to_s.should == 'http://dbpedialite.org/things/52780#thing'
    end
  end

  context "creating an thing from a non-existant page title" do
    before :each do
      WikipediaApi.expects(:query).once.returns({'zsefpfs'=>{"title"=>"zsefpfs", "ns"=>0, "missing"=>""}})
      @thing = WikipediaThing.for_title('zsefpfs')
    end

    it "should return an object of type WikipediaThing" do
      @thing.should == nil
    end
  end

  context "creating an thing with data provided" do
    before :each do
      WikipediaApi.expects(:query).never
      @thing = WikipediaThing.for(934787,
        :title => 'Ceres, Fife',
        :latitude => 56.293431,
        :longitude => -2.970134,
        :updated_at => DateTime.parse('2010-05-08T17:20:04Z'),
        :abstract => "Ceres is a village in Fife, Scotland."
      )
      # FIXME: This is a hack to make sure the setter method gets called
      @thing.title = 'Ceres, Fife'
    end

    it "should return an object of type WikipediaThing" do
      @thing.class.should == WikipediaThing
    end

    it "should have the correct URI" do
      @thing.uri.to_s.should == 'http://dbpedialite.org/things/934787#thing'
    end

    it "should have the correct title" do
      @thing.title.should == 'Ceres, Fife'
    end

    it "should have the correct abstract" do
      @thing.abstract.should == 'Ceres is a village in Fife, Scotland.'
    end

    it "should have a pageid method to get the page id from the uri" do
      @thing.pageid.should == 934787
    end

    it "should have the correct latitude" do
      @thing.latitude.should == 56.293431
    end

    it "should have the correct longitude" do
      @thing.longitude.should == -2.970134
    end

    it "should encode the Wikipedia page URL correctly" do
      @thing.page.to_s.should == 'http://en.wikipedia.org/wiki/Ceres%2C_Fife'
    end

    it "should encode the dbpedia URI correctly" do
      @thing.dbpedia.to_s.should == 'http://dbpedia.org/resource/Ceres%2C_Fife'
    end
  end

  context "loading a page from wikipedia" do
    before :each do
      data = {'title' => 'Ceres, Fife',
              'longitude' => -2.970134,
              'latitude' => 56.293431,
              'valid' => true,
              'abstract' => 'Ceres is a village in Fife, Scotland'
             }
      WikipediaApi.expects(:query).never
      WikipediaApi.expects(:parse).once.returns(data)
      @thing = WikipediaThing.load(934787)
    end

    it "should return a WikipediaThing" do
      @thing.class.should == WikipediaThing
    end

    it "should had the correct page id" do
      @thing.pageid.should == 934787
    end

    it "should had the correct title" do
      @thing.title.should == 'Ceres, Fife'
    end

    it "should have co-ordinates" do
      @thing.should have_coordinates
    end

    it "should have the correct latitude" do
      @thing.latitude.should == 56.293431
    end

    it "should have the correct longitude" do
      @thing.longitude.should == -2.970134
    end

    it "should escape titles correctly" do
      @thing.escaped_title.should == 'Ceres%2C_Fife'
    end

    it "should encode the Wikipedia page URL correctly" do
      @thing.page.to_s.should == 'http://en.wikipedia.org/wiki/Ceres%2C_Fife'
    end

    it "should encode the dbpedia URI correctly" do
      @thing.dbpedia.to_s.should == 'http://dbpedia.org/resource/Ceres%2C_Fife'
    end

    it "should extract the abstract correctly" do
      @thing.abstract.should =~ /^Ceres is a village in Fife, Scotland/
    end
  end

  context "loading a non-existant page from wikipedia" do
    before :each do
      data = {'valid' => false}
      WikipediaApi.expects(:query).never
      WikipediaApi.expects(:parse).once.returns(data)
      @thing = WikipediaThing.load(999999)
    end

    it "should return nil" do
      @thing.should == nil
    end
  end

  context "serializing an thing to N-Triples" do
    before :each do
      WikipediaApi.expects(:query).never
      @thing = WikipediaThing.for(52780,
        :title => 'U2',
        :abstract => "U2 are an Irish rock band."
      )
      @ntriples = @thing.dump(:ntriples)
    end

    it "should serialise to a string" do
      @ntriples.class.should == String
    end

    it "should serialise to 3 triples" do
      @ntriples.split(/[\r\n]+/).count.should == 3
    end
  end
end