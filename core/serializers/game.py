from rest_framework import serializers

from core.models import Game
from core.models.description import Description
from core.models.developer import Developer
from core.models.feature import Feature
from core.models.genre import Genre
from core.models.picture import Picture
from core.models.price import Price
from core.models.publisher import Publisher
from core.models.specification import Specification
from core.models.video import Video
from core.serializers.description import DescriptionSerializer
from core.serializers.developer import DeveloperSerializer
from core.serializers.feature import FeatureSerializer
from core.serializers.genre import GenreSerializer
from core.serializers.picture import PictureSerializer
from core.serializers.price import PriceSerializer
from core.serializers.publisher import PublisherSerializer
from core.serializers.specification import SpecificationSerializer
from core.serializers.video import VideoSerializer


class GameSerializer(serializers.ModelSerializer):

    description = DescriptionSerializer()
    specification = SpecificationSerializer()

    developers = DeveloperSerializer(many=True)
    features = FeatureSerializer(many=True)
    genres = GenreSerializer(many=True)
    pictures = PictureSerializer(many=True)
    publishers = PublisherSerializer(many=True)
    videos = VideoSerializer(many=True)

    prices = PriceSerializer(many=True)

    class Meta:
        model = Game
        fields = '__all__'


    def create(self, validated_data):
        developers_data = validated_data.pop('developers')
        publishers_data = validated_data.pop('publishers')
        features_data = validated_data.pop('features')
        genres_data = validated_data.pop('genres')
        pictures_data = validated_data.pop('pictures')
        videos_data = validated_data.pop('videos')

        description_data = validated_data.pop('description')
        prices_data = validated_data.pop('prices')
        specification_data = validated_data.pop('specification')

        game = Game.objects.create(**validated_data)

        desc = Description.objects.create(game=game, **description_data)
        game.description_id = desc.id

        spec = Specification.objects.create(game=game, **specification_data)
        game.specification_id = spec.id

        for price_data in prices_data:
            Price.objects.create(game=game, **price_data)
        for developer_data in developers_data:
            Developer.objects.create(game=game, **developer_data)
        for publisher_data in publishers_data:
            Publisher.objects.create(game=game, **publisher_data)
        for feature_data in features_data:
            Feature.objects.create(game=game, **feature_data)
        for genre_data in genres_data:
            Genre.objects.create(game=game, **genre_data)
        for picture_data in pictures_data:
            Picture.objects.create(game=game, **picture_data)
        for video_data in videos_data:
            Video.objects.create(game=game, **video_data)

        game.save()
        return game

    # def create(self, validated_data):
    #     return self.generic(validated_data)
        # data = validated_data
        #
        # new_game = Game.objects.get_or_create(
        #     name=data['name'],
        #     thumbnail=data['thumbnail'],
        #     releaseDate=data['releaseDate'],
        #     description=data['description'],
        #     specification=data['specification'],
        #     prices=data['prices']
        # )
        #
        # new_game.save()
        #
        # for developer in data['developers']:
        #     developer_obj = Developer.objects.get(name=developer['name'])
        #     new_game.developer.add(developer_obj)
        # for developer in data['publishers']:
        #     developer_obj = Publisher.objects.get(name=developer['name'])
        #     new_game.developer.add(developer_obj)
        #
        # for developer in data['videos']:
        #     developer_obj = Video.objects.get(url=developer['url'])
        #     new_game.developer.add(developer_obj)
        # for developer in data['pictures']:
        #     developer_obj = Picture.objects.get(url=developer['url'])
        #     new_game.developer.add(developer_obj)
        #
        # for developer in data['features']:
        #     developer_obj = Feature.objects.get(title=developer['title'])
        #     new_game.developer.add(developer_obj)
        # for developer in data['genres']:
        #     developer_obj = Genre.objects.get(title=developer['title'])
        #     new_game.developer.add(developer_obj)
        #
        # return new_game

    # def generic(self, validated_data):
    #     for key, value in self._MODELS.items():
    #         tmp_valid_data = validated_data.pop(key, None)
    #         if tmp_valid_data:
    #             if type(tmp_valid_data) == list:
    #                 tmp = Game.objects.create()
    #                 for item in tmp_valid_data:
    #                     tmp.add(item.save())
    #                 validated_data[key] = tmp
    #             else:
    #                 tmp_obj = value.objects.get_or_create(**tmp_valid_data)[0]
    #                 validated_data[key] = tmp_obj
    #     return Game.objects.create(**validated_data)

