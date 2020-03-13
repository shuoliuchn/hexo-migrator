from django.db import models


class BlogModel(models.Model):
    title = models.CharField(max_length=100, verbose_name='博客标题')
    # 相对于博客根路径 settings.BLOG_BASE_DIR
    path = models.CharField(max_length=200, verbose_name='博客相对路径', unique=True, db_index=True)
    categories = models.ForeignKey(to='CategoriesModel', verbose_name='博客分类', on_delete=models.DO_NOTHING, null=True)
    tags = models.ManyToManyField(to='TagsModel', verbose_name='博客标签', blank=True)
    is_valid = models.BooleanField(default=True, verbose_name='是否有效')
    is_mathjax = models.BooleanField(default=False, verbose_name='是否启用 mathjax 数学公式')
    allow_comments = models.BooleanField(default=True, verbose_name='是否允许评论')
    is_top = models.BooleanField(default=False, verbose_name='是否首页置顶（需配合 hexo-generator-index-pin-top 使用）')
    layout = models.CharField(max_length=100, default='single-column', verbose_name='输出模式（Next 模板无需设置）', null=True, blank=True)
    is_toc = models.BooleanField(default=True, verbose_name='是否展示目录（Next 模板无需设置）')
    date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    description = models.CharField(max_length=1000, verbose_name='博客描述', null=True, blank=True)
    content = models.TextField(verbose_name='博客内容', null=True, blank=True)

    @property
    def show_tags(self):
        tags = '，'.join(self.tag_list)
        return tags

    @property
    def tag_list(self):
        return [tag.tag_name for tag in self.tags.filter(is_valid=True)]

    @property
    def categories_name(self):
        return self.categories.category_name if self.categories else ''

    def __str__(self):
        return self.title


class TagsModel(models.Model):
    is_valid = models.BooleanField(default=True, verbose_name='是否有效')
    tag_name = models.CharField(max_length=50, verbose_name='标签名')

    def __str__(self):
        return self.tag_name


class CategoriesModel(models.Model):
    wrapper_folder = models.CharField(max_length=100, verbose_name='外层文件夹名', unique=True)
    category_name = models.CharField(max_length=50, verbose_name='分类名称')
    is_valid = models.BooleanField('是否有效', default=True)

    def __str__(self):
        return self.category_name
