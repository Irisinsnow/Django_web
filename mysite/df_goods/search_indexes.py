from haystack import indexes
from df_goods.models import Goods


class GoodsIndex(indexes.SearchIndex, indexes.Indexable):
    # 索引字段
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Goods

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
