SELECT  "shopapp_product"."id",
        "shopapp_product"."created_by_id",
        "shopapp_product"."name",
        "shopapp_product"."description",
        "shopapp_product"."price",
        "shopapp_product"."discount",
        "shopapp_product"."created_at",
        "shopapp_product"."archived",
        "shopapp_product"."preview"
FROM "shopapp_product"
WHERE NOT "shopapp_product"."archived"
ORDER BY "shopapp_product"."name" ASC,
         "shopapp_product"."price" ASC;

SELECT  "shopapp_product"."id",
        "shopapp_product"."created_by_id",
        "shopapp_product"."name",
        "shopapp_product"."description",
        "shopapp_product"."price",
        "shopapp_product"."discount",
        "shopapp_product"."created_at",
        "shopapp_product"."archived",
        "shopapp_product"."preview"
FROM "shopapp_product"
WHERE "shopapp_product"."id" = 16
LIMIT 21;

SELECT "shopapp_productimage"."id",
        "shopapp_productimage"."product_id",
        "shopapp_productimage"."image",
        "shopapp_productimage"."description"
FROM "shopapp_productimage"
WHERE "shopapp_productimage"."product_id" IN (16);


SELECT "django_session"."session_key",
        "django_session"."session_data",
        "django_session"."expire_date"
FROM "django_session"
WHERE ("django_session"."expire_date" > '2023-08-19 09:14:24.203064' AND
        "django_session"."session_key" = 'fhgdaoo8loz9hb9jh2ddwry5qbwgq7li')
LIMIT 21;

SELECT "auth_user"."id",
        "auth_user"."password",
        "auth_user"."last_login",
        "auth_user"."is_superuser",
        "auth_user"."username",
        "auth_user"."first_name",
        "auth_user"."last_name",
        "auth_user"."email",
        "auth_user"."is_staff",
        "auth_user"."is_active",
        "auth_user"."date_joined"
FROM "auth_user"
WHERE "auth_user"."id" = 1
LIMIT 21;

SELECT "shopapp_order"."id",
        "shopapp_order"."delivery_address",
        "shopapp_order"."pomocode",
        "shopapp_order"."created_at",
        "shopapp_order"."user_id",
        "shopapp_order"."receipt",
        "auth_user"."id",
        "auth_user"."password",
        "auth_user"."last_login",
        "auth_user"."is_superuser",
        "auth_user"."username",
        "auth_user"."first_name",
        "auth_user"."last_name",
        "auth_user"."email",
        "auth_user"."is_staff",
        "auth_user"."is_active",
        "auth_user"."date_joined"
FROM "shopapp_order"
INNER JOIN "auth_user" ON ("shopapp_order"."user_id" = "auth_user"."id");


SELECT ("shopapp_order_products"."order_id") AS "_prefetch_related_val_order_id",
        "shopapp_product"."id",
        "shopapp_product"."created_by_id",
        "shopapp_product"."name",
        "shopapp_product"."description",
        "shopapp_product"."price",
        "shopapp_product"."discount",
        "shopapp_product"."created_at",
        "shopapp_product"."archived",
        "shopapp_product"."preview"
FROM "shopapp_product"
INNER JOIN "shopapp_order_products" ON ("shopapp_product"."id" = "shopapp_order_products"."product_id")
WHERE "shopapp_order_products"."order_id" IN (1, 2, 4, 7)
ORDER BY "shopapp_product"."name" ASC,
        "shopapp_product"."price" ASC;

--===============================================

SELECT "django_session"."session_key",
        "django_session"."session_data",
        "django_session"."expire_date"
FROM "django_session"
WHERE ("django_session"."expire_date" > '2023-08-19 10:11:23.683369' AND
        "django_session"."session_key" = 'fhgdaoo8loz9hb9jh2ddwry5qbwgq7li')
LIMIT 21;

SELECT "auth_user"."id",
        "auth_user"."password",
        "auth_user"."last_login",
        "auth_user"."is_superuser",
        "auth_user"."username",
        "auth_user"."first_name",
        "auth_user"."last_name",
        "auth_user"."email",
        "auth_user"."is_staff",
        "auth_user"."is_active",
        "auth_user"."date_joined"
FROM "auth_user"
WHERE "auth_user"."id" = 1
LIMIT 21;

SELECT "shopapp_order"."id",
        "shopapp_order"."delivery_address",
        "shopapp_order"."pomocode",
        "shopapp_order"."created_at",
        "shopapp_order"."user_id",
        "shopapp_order"."receipt",
        "auth_user"."id",
        "auth_user"."password",
        "auth_user"."last_login",
        "auth_user"."is_superuser",
        "auth_user"."username",
        "auth_user"."first_name",
        "auth_user"."last_name",
        "auth_user"."email",
        "auth_user"."is_staff",
        "auth_user"."is_active",
        "auth_user"."date_joined"
FROM "shopapp_order"
INNER JOIN "auth_user" ON ("shopapp_order"."user_id" = "auth_user"."id");

SELECT ("shopapp_order_products"."order_id") AS "_prefetch_related_val_order_id",
"shopapp_product"."id", "shopapp_product"."created_by_id", "shopapp_product"."name", "shopap
p_product"."description", "shopapp_product"."price", "shopapp_product"."discount", "shopapp_product"."created_at", "shopapp_product"."archived", "shopapp_product"."preview" FROM "sho
papp_product" INNER JOIN "shopapp_order_products" ON ("shopapp_product"."id" = "shopapp_order_products"."product_id") WHERE "shopapp_order_products"."order_id" IN (1, 2, 4, 7) ORDER
BY "shopapp_product"."name" ASC, "shopapp_product"."price" ASC; args=(1, 2, 4, 7); alias=default



----
SELECT "blogapp_article"."id",
        "blogapp_article"."title",
        "blogapp_article"."content",
        "blogapp_article"."pub_date",
        "blogapp_article"."author_id"
FROM "blogapp_article"

SELECT "blogapp_author"."id",
        "blogapp_author"."name",
        "blogapp_author"."bio"
FROM "blogapp_author"
WHERE "blogapp_author"."id" = 1
LIMIT 21

SELECT "blogapp_tag"."id",
        "blogapp_tag"."name"
FROM "blogapp_tag"
INNER JOIN "blogapp_article_tags" ON ("blogapp_tag"."id" = "blogapp_article_tags"."tag_id")
WHERE "blogapp_article_tags"."article_id" = 1

SELECT "blogapp_author"."id",
        "blogapp_author"."name",
        "blogapp_author"."bio"
FROM "blogapp_author"
WHERE "blogapp_author"."id" = 2
LIMIT 21

SELECT "blogapp_tag"."id",
        "blogapp_tag"."name"
FROM "blogapp_tag"
INNER JOIN "blogapp_article_tags" ON ("blogapp_tag"."id" = "blogapp_article_tags"."tag_id")
WHERE "blogapp_article_tags"."article_id" = 2;

SELECT "blogapp_author"."id",
        "blogapp_author"."name",
        "blogapp_author"."bio"
FROM "blogapp_author"
WHERE "blogapp_author"."id" = 2
LIMIT 21

SELECT "blogapp_tag"."id",
        "blogapp_tag"."name"
FROM "blogapp_tag"
INNER JOIN "blogapp_article_tags" ON ("blogapp_tag"."id" = "blogapp_article_tags"."tag_id")
WHERE "blogapp_article_tags"."article_id" = 3


---
SELECT "blogapp_article"."id",
        "blogapp_article"."title",
        "blogapp_article"."content",
        "blogapp_article"."pub_date",
        "blogapp_article"."author_id",
        "blogapp_author"."id",
        "blogapp_author"."name",
        "blogapp_author"."bio"
FROM "blogapp_article"
INNER JOIN "blogapp_author" ON ("blogapp_article"."author_id" = "blogapp_author"."id")

SELECT "blogapp_tag"."id",
        "blogapp_tag"."name"
FROM "blogapp_tag"
INNER JOIN "blogapp_article_tags" ON ("blogapp_tag"."id" = "blogapp_article_tags"."tag_id")
WHERE "blogapp_article_tags"."article_id" = 1

SELECT "blogapp_tag"."id",
        "blogapp_tag"."name"
FROM "blogapp_tag"
INNER JOIN "blogapp_article_tags" ON ("blogapp_tag"."id" = "blogapp_article_tags"."tag_id")
WHERE "blogapp_article_tags"."article_id" = 2

SELECT "blogapp_tag"."id",
        "blogapp_tag"."name"
FROM "blogapp_tag"
INNER JOIN "blogapp_article_tags" ON ("blogapp_tag"."id" = "blogapp_article_tags"."tag_id")
WHERE "blogapp_article_tags"."article_id" = 3

-----
SELECT "blogapp_article"."id",
        "blogapp_article"."title",
        "blogapp_article"."content",
        "blogapp_article"."pub_date",
        "blogapp_article"."author_id",
        "blogapp_author"."id",
        "blogapp_author"."name",
        "blogapp_author"."bio"
FROM "blogapp_article"
    INNER JOIN "blogapp_author" ON ("blogapp_article"."author_id" = "blogapp_author"."id")

SELECT ("blogapp_article_tags"."article_id")
    AS "_prefetch_related_val_article_id", "blogapp_tag"."id", "blogapp_tag"."name"
    FROM "blogapp_tag"
    INNER JOIN "blogapp_article_tags" ON ("blogapp_tag"."id" = "blogapp_article_tags"."tag_id")
WHERE "blogapp_article_tags"."article_id" IN (1, 2, 3)
